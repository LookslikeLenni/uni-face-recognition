from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile, File, Response
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.types import TypeDecorator, TEXT
from sqlalchemy.ext.mutable import MutableList
from pydantic import BaseModel, Field
from typing import List
import base64
import json
from io import BytesIO
import zipfile
import uvicorn
from os import listdir
from os.path import join
import cv2
import numpy as np
import sys

from video_handler import DetectFaces

expected_embedding_sizes = {
    "VGG-Face": 4096,
    "Facenet": 128,
    "Facenet512": 512,
    "OpenFace": 128,
    "DeepFace": 4096,
    "DeepID": 160,
    "ArcFace": 512,
    "Dlib": 128,
    "SFace": 512,
    "GhostFaceNet": 512,
}

backends = [
    'opencv', 
    'ssd', 
    'dlib', 
    'mtcnn', 
    'fastmtcnn',
    'retinaface', 
    'mediapipe',
    'yolov8',
    'yunet',
    'centerface',
]

metrics = ["cosine", "euclidean", "euclidean_l2"]

models = [
    "VGG-Face", 
    "Facenet", 
    "Facenet512", 
    "OpenFace", 
    "DeepFace", 
    "DeepID", 
    "ArcFace", 
    "Dlib", 
    "SFace",
    "GhostFaceNet",
]

model_used = 2

rec = DetectFaces(
        model = model_used,
        metric = 0,
        backend = 8,
        cap_dev = 0,
        threshold = 0.3
    )

templates = Jinja2Templates(directory=".")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    embedding = Column(MutableList.as_mutable(Json), default=[])

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

def gen_frames():
    db = SessionLocal()
    while True:
        frame, faces = rec.get_frame()
        for name, face in faces:
            if(name == "Unknown"):
                max_id = db.query(func.max(User.id)).scalar() or 0
                emb = rec.add_image(f'Unknown  {max_id+1}', face)
                if emb:
                    _, buffer = cv2.imencode('.jpg', face)
                    image_data = base64.b64encode(buffer).decode('utf-8')
                    new_user = User(first_name="Unknown", last_name="", greeting="Automatically added unknown face", images=[image_data], embedding=emb)
                    db.add(new_user)
                    db.commit()
              
            elif face is not None:
                for z in name.split():
                    if z.isdigit():
                        user_id = z
                print(f"adding new db image to user {user_id}")
                try:
                    db_user = db.query(User).filter(User.id == user_id).first()
                    _, buffer = cv2.imencode('.jpg', face)
                    image_data = base64.b64encode(buffer).decode('utf-8')
                    db_user.images.append(image_data)
                    db.commit()
                except Exception as e:
                    print(f"could not add image to user: {get_user_name(db_user.id)}, {e}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
async def add_images_to_user(user_id: int, image_files: List[UploadFile] = File(..., multiple=True), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for image_file in image_files:
        if not image_file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Invalid file type. Only image files are allowed")

        image = await image_file.read()
        image_data = base64.b64encode(image).decode('utf-8')
        db_user.images.append(image_data)
        db.commit()

        img_array = np.frombuffer(image, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        name = get_user_name(user_id)
        rec.add_image(name, img)

    return db_user

@app.delete("/users/{user_id}/", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    full_name = get_user_name(db_user.id)
    rec.del_user(full_name)

    db.delete(db_user)
    db.commit()
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
  
    rec.edit_user_name(get_user_name(user_id), f'{user_update.first_name} {user_update.last_name} {user_id}')

    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()

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
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":

    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        if not user.embedding or '-r' in sys.argv or len(user.embedding) != expected_embedding_sizes.get(models[model_used]):
            images = user.images
            for image in images:
                img_bytes = base64.b64decode(image)
                img_array = np.frombuffer(img_bytes, dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                emb = rec.add_image(get_user_name(user.id), img)
                if(emb):
                    user.embedding = emb
                print(f'added image for user: {get_user_name(user.id)}')
        else:
            rec.add_embedding(get_user_name(user.id), user.embedding) 
            print(f'added embedding for user: {get_user_name(user.id)}')
    db.commit()

    uvicorn.run(app, host="0.0.0.0", port=8000)
