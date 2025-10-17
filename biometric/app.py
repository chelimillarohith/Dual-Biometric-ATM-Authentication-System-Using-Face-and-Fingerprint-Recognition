# app.py
import streamlit as st
import sqlite3
from encryption import encrypt, decrypt
from fingerprint_recog import get_fingerprint_features, verify_fingerprint
from face_recog import register_face, verify_face

DB_FILE = "biometrics.db"

# Initialize DB
conn = sqlite3.connect(DB_FILE)
conn.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    fingerprint_enc TEXT,
    face_enc BLOB
)''')
conn.close()

st.set_page_config(page_title="Biometric ATM System", page_icon="💳")
st.title("💳 Biometric ATM Security System")
st.markdown("### Authenticate using Fingerprint + Face Recognition")

menu = st.sidebar.radio("Navigation", ["Register User", "Authenticate User"])
username = st.text_input("Enter Username:")

if menu == "Register User":
    st.subheader("Register Fingerprint and Face")

    fingerprint_file = st.file_uploader("Upload Fingerprint Image", type=["png", "jpg", "jpeg"])
    face_capture = st.camera_input("Capture Face Image")

    if st.button("Register"):
        if username and fingerprint_file and face_capture:
            # Encrypt fingerprint
            fingerprint_data = fingerprint_file.read()
            encrypted_fp = encrypt(fingerprint_data)

            # Get face encoding
            face_encoding = register_face(face_capture)

            conn = sqlite3.connect(DB_FILE)
            conn.execute("INSERT OR REPLACE INTO users (username, fingerprint_enc, face_enc) VALUES (?, ?, ?)",
                         (username, encrypted_fp, face_encoding))
            conn.commit()
            conn.close()
            st.success(f"✅ User '{username}' registered successfully!")
        else:
            st.error("Please enter username, upload fingerprint and capture face.")

elif menu == "Authenticate User":
    st.subheader("Authenticate Fingerprint and Face")

    fingerprint_file = st.file_uploader("Upload Fingerprint Image for Verification", type=["png", "jpg", "jpeg"])
    face_capture = st.camera_input("Capture Face for Verification")

    if st.button("Authenticate"):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.execute("SELECT fingerprint_enc, face_enc FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            st.error("User not found!")
        else:
            stored_fp_enc, stored_face_enc = user
            stored_fp = decrypt(stored_fp_enc)
            fp_match = verify_fingerprint(stored_fp, fingerprint_file.read())
            face_match = verify_face(stored_face_enc, face_capture)

            if fp_match and face_match:
                st.success("✅ Authentication Successful — Access Granted!")
            else:
                st.error("❌ Authentication Failed — Mismatch detected.")
