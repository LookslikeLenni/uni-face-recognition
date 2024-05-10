from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile, File, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import func
from pydantic import BaseModel, Field
from typing import List
import base64
import json
import time
from io import BytesIO
import zipfile
import uvicorn
import face_recognition
from os import listdir
from os.path import join
import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []
face_locations = []
face_encodings = []
face_names = []

scale = 1

templates = Jinja2Templates(directory=".")

app = FastAPI()

# Database configuration
DATABASE_URL = "sqlite:///./user.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Custom JSON type decorator for automatic JSON encoding/decoding
class Json(TypeDecorator):
    impl = TEXT
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)

# Database model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    greeting = Column(Text)
    images = Column(MutableList.as_mutable(Json), default=[])

Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    greeting: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    greeting: str
    images: List[str]

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserUpdate(BaseModel):
    first_name: str = Field(default=None, example="Jane")
    last_name: str = Field(default=None, example="Doe")
    greeting: str = Field(default=None, example="Hello, welcome to my updated profile!")

def get_images_from_db():
    db = SessionLocal()
    users = db.query(User).all()
    images = []
    for user in users:
        for img_data in user.images:
            img_bytes = base64.b64decode(img_data)
            img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            images.append((f"{user.first_name} {user.last_name} {user.id}", img))
    db.close()
    return images

def get_user_name(user_id: int) -> str:
    """Retrieve the first and last name of a user by their ID."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return f"{user.first_name} {user.last_name} {user.id}"
        else:
            return "User not found"
    finally:
        db.close()

def gen_frames(db: Session):
    prev_frame_time = 0
    new_frame_time = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    fps = 0

    while True:
        new_frame_time = time.time() 
        new_fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time
        new_fps = int(new_fps) 
        if(abs(new_fps-fps) > 3):
          fps = new_fps

        ret, frame = video_capture.read()
        cv2.putText(frame, str(fps), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
        if not ret:
            break
        else:
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"
                
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= int(1/scale)
                right *= int(1/scale)
                bottom *= int(1/scale)
                left *= int(1/scale)
                
                if True in matches:
                    best_match_index = np.argmin(face_recognition.face_distance(known_face_encodings, face_encoding))
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                else:
                    # Save the new user if it's an unknown face
                    name, face_encoding = add_new_user(face_encoding, frame[top:bottom, left:right], db)

                # Draw the results
                draw_face_box(frame, top, right, bottom, left, name)

            # Encode frame for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def add_new_user(face_encoding, face_image, db: Session):
    try:
        _, buffer = cv2.imencode('.jpg', face_image)
        image_data = base64.b64encode(buffer).decode('utf-8')

        max_id = db.query(func.max(User.id)).scalar() or 0
        new_user = User(first_name="Unknown", last_name="", greeting="Automatically added unknown face", images=[image_data])
        
        db.add(new_user)
        db.commit()

        new_user_name = get_user_name(max_id+1)

        known_face_encodings.append(face_encoding)
        known_face_names.append(new_user_name)

        return new_user_name, face_encoding
    except Exception as e:
        print(f"Failed to add new user: {str(e)}")
        return "Failed User", None

def draw_face_box(frame, top, right, bottom, left, name):
    # Draw a box around the face using the coordinates provided
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    font_scale = 1.5
    font_thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_width, text_height = cv2.getTextSize(name, font, font_scale, font_thickness)[0]
    box_coords = ((left, bottom + 10), (left + text_width, bottom - text_height - 10))
    cv2.rectangle(frame, box_coords[0], box_coords[1], (0, 0, 255), cv2.FILLED)
    cv2.putText(frame, name, (left + 6, bottom - 6), font, font_scale, (255, 255, 255), font_thickness)

# API Endpoints
@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        greeting=user.greeting
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users/{user_id}/images/", response_model=UserOut)
async def add_image_to_user(user_id: int, image_file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not image_file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only image files are allowed.")

    image_data = base64.b64encode(await image_file.read()).decode('utf-8')
    db_user.images.append(image_data)
    db.commit()

    img_bytes = base64.b64decode(image_data)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    encoding = face_recognition.face_encodings(img)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(get_user_name(user_id))

    return db_user

@app.delete("/users/{user_id}/", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    full_name = get_user_name(user_id)
    for full_name in known_face_names:
      index = known_face_names.index(full_name)
      known_face_names.pop(index)
      known_face_encodings.pop(index)
    return {"msg": "User deleted"}

@app.get("/users/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}/", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}/images/")
def remove_image_from_user(user_id: int, image_index: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        images = db_user.images
        if images and 0 <= image_index < len(images):
            images.pop(image_index)
            db_user.images = images
            db.commit()
            return JSONResponse(content={"msg": "Image removed successfully"})
        else:
            raise HTTPException(status_code=404, detail="Image index out of range")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/images/zip/")
def get_images_zip(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    images = db_user.images
    if not images:
        raise HTTPException(status_code=404, detail="No images available for this user")

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for idx, img_data in enumerate(images):
            img_bytes = base64.b64decode(img_data)
            zip_file.writestr(f'image_{idx}.jpg', img_bytes)
    zip_buffer.seek(0)

    return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": f"attachment;filename={db_user.first_name}_images.zip"})

@app.put("/users/{user_id}/", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    index = []
    full_name = get_user_name(user_id)
    for i, name in enumerate(known_face_names):
        if(name == full_name):
          index.append(i)

    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()

    full_name = get_user_name(user_id)
    for i in index:
        known_face_names[i] = full_name
    return db_user

@app.get("/users/{user_id}/images/{image_index}/")
def get_user_image(user_id: int, image_index: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        images = user.images
        if image_index < 0 or image_index >= len(images):
            raise HTTPException(status_code=404, detail="Image index out of range")
        
        image_data = images[image_index]
        image_bytes = base64.b64decode(image_data)
        return Response(content=image_bytes, media_type='image/jpeg')
    except IndexError:
        raise HTTPException(status_code=404, detail="Image index out of range")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/video_feed')
def video_feed(db: Session = Depends(get_db)):
    return StreamingResponse(gen_frames(db), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":

    images = get_images_from_db()
    for name, img in images:
        try:
            encoding = face_recognition.face_encodings(img)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)
        except Exception as e:
            print(f"could not add {name}: {e}") 

    uvicorn.run(app, host="127.0.0.1", port=8000)
