# face_recog.py
import face_recognition
import numpy as np
import pickle

def register_face(face_img):
    img = face_recognition.load_image_file(face_img)
    encodings = face_recognition.face_encodings(img)
    if len(encodings) == 0:
        raise ValueError("No face detected.")
    return pickle.dumps(encodings[0])

def verify_face(stored_encoding, captured_face_img):
    known_encoding = pickle.loads(stored_encoding)
    img = face_recognition.load_image_file(captured_face_img)
    encodings = face_recognition.face_encodings(img)
    if len(encodings) == 0:
        return False
    return face_recognition.compare_faces([known_encoding], encodings[0])[0]
