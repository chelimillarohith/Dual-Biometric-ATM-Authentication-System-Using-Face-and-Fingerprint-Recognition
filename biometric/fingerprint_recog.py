# fingerprint_recog.py
import cv2
import numpy as np
import pickle

def get_fingerprint_features(img_bytes):
    np_bytes = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_bytes, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create(nfeatures=1000)
    kp, des = orb.detectAndCompute(img, None)
    return pickle.dumps(des)

def verify_fingerprint(stored_fp, uploaded_fp_bytes, min_matches=10):
    stored_np = np.frombuffer(stored_fp, np.uint8)
    stored_img = cv2.imdecode(stored_np, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(stored_img, None)

    np_bytes = np.frombuffer(uploaded_fp_bytes, np.uint8)
    img2 = cv2.imdecode(np_bytes, cv2.IMREAD_GRAYSCALE)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return False

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    good = [m for m in matches if m.distance < 60]
    return len(good) >= min_matches
