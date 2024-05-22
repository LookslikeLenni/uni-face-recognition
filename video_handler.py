from deepface import DeepFace
import numpy as np
import cv2

unknown_face_counter = 0
isknown = False
counter_threshold = 10

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

class DetectFaces:
    def __init__(self, cap_dev=0, model: int = 0, metric: int = 0, backend: int = 0, threshold=0.3):
        self.cap = cv2.VideoCapture(cap_dev)
        self.model = models[model]
        self.metric = metrics[metric]
        self.backend = backends[backend]
        self.threshold = threshold
        self.known_embeddings = []

    def edit_user_name(self, old_name: str, new_name: str):
        self.known_embeddings = [(new_name if name == old_name else name, x) for name, x in self.known_embeddings]

    def del_user(self, rm_name: str):
        print(f'removing {rm_name}')
        self.known_embeddings = [(name, x) for name, x in self.known_embeddings if name != rm_name]

    def add_embedding(self, img_name: str, embedding):
        for name, emb in self.known_embeddings:
            if(name == img_name):
                print(f"Error user: {name} exists already")
        self.known_embeddings.append((img_name, embedding))

    def add_image(self, name: str, img: np.ndarray):
        try:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            embedding = DeepFace.represent(
                img_path=img,
                model_name=self.model,
                detector_backend=self.backend,
                enforce_detection=False,
            )[0]['embedding']
            for img_name, emb in self.known_embeddings:
                if(img_name == name):
                    combined = np.mean([embedding, emb], axis=0).tolist()
                    self.known_embeddings.remove((img_name, emb))
                    self.known_embeddings.append((img_name, combined))
                    print(f"image added to: {name}")
                    return combined
            self.known_embeddings.append((name, embedding))
            print(f"created: {name} and added image")
            return embedding
        except Exception as e:
            print(f"could not add image: {e}")
            return None

    def get_frame(self):
        ret, frame_rgb = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return None, []

        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        current_faces = []
        faces = []
        try:
            faces = DeepFace.extract_faces(img_path=frame, detector_backend=self.backend, enforce_detection=False)
        except Exception as e:
            print(f"Error in face extraction: {e}")

        for face in faces:
            face_region = face['face']
            facial_area = face['facial_area']

            x = facial_area['x']
            y = facial_area['y']
            w = facial_area['w']
            h = facial_area['h']

            if face_region.dtype != np.uint8:
                face_region = cv2.convertScaleAbs(face_region, alpha=(255.0))

            #face_region = face_region.astype(np.uint8)
            embedding = None
            try:
                embedding = DeepFace.represent(
                    img_path=face_region,
                    model_name=self.model,
                    detector_backend=self.backend,
                    enforce_detection=False,
                )[0]['embedding']
            except Exception as e:
                print(f"Error in represent: {e}")

            name = 'Unknown'
            color = (0, 0, 255)  # Red for unknown

            global isknown
            global counter_threshold
            global unknown_face_counter

            for known_name, known_embedding in self.known_embeddings:
                try:
                    if(embedding and known_embedding):
                        verify = DeepFace.verify(
                            img1_path=embedding,
                            img2_path=known_embedding,
                            model_name=self.model,
                            distance_metric=self.metric,
                            threshold = self.threshold,
                            normalization = 'Facenet',
                            silent = True,
                            enforce_detection=False,
                        )
                    if(verify['verified'] == True):
                        color = (0, 255, 0)
                        name = known_name
                        isknown = True
                        if(verify['distance']>(self.threshold-(self.threshold/2.5))):
                            self.add_image(name, face_region)
                            current_faces.append((name, face_region))
                        else:
                            current_faces.append((name, None))
                        break
                    else:
                      isknown = False
                except Exception as e:
                    print(f"Error in verification: {e}")

            if(unknown_face_counter >= 0):
                unknown_face_counter -= 0.2

            if not isknown:
                unknown_face_counter += 1

            if unknown_face_counter >= counter_threshold:
                unknown_face_counter = 0
                current_faces.append((name, face_region))

            cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), color, 4)
            cv2.putText(frame_rgb, name, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        return (frame_rgb, current_faces)
