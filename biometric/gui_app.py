# gui_app.py
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from encryption import encrypt, decrypt

DB_FILE = "finger_users.db"
IMG_DIR = "fingerprint_samples"

# Create DB if not exists
conn = sqlite3.connect(DB_FILE)
conn.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    encrypted_fingerprint TEXT NOT NULL
)''')
conn.close()

def encrypt_image(image_path):
    with open(image_path, 'rb') as f:
        raw_data = f.read()
    return encrypt(raw_data)

def compare_images(img1, img2):
    return img1 == img2

def register_user():
    username = username_entry.get()
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not file_path or not username:
        messagebox.showerror("Error", "Please enter username and select fingerprint image.")
        return

    encrypted_data = encrypt_image(file_path)

    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("INSERT INTO users (username, encrypted_fingerprint) VALUES (?, ?)", (username, encrypted_data))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"{username} registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

def authenticate_user():
    username = username_entry.get()
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not file_path or not username:
        messagebox.showerror("Error", "Please enter username and select fingerprint image.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT encrypted_fingerprint FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        messagebox.showerror("Error", "User not found.")
        return

    stored_enc = row[0]
    stored_img = decrypt(stored_enc)

    with open(file_path, 'rb') as f:
        input_img = f.read()

    if compare_images(stored_img, input_img):
        messagebox.showinfo("Access Granted", "Fingerprint matched. Access granted!")
    else:
        messagebox.showerror("Access Denied", "Fingerprint does not match.")

# GUI
root = tk.Tk()
root.title("Biometric ATM - Fingerprint Security")
root.geometry("400x300")  

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

title = tk.Label(frame, text="Fingerprint-Based ATM Authentication", font=("Arial", 14, "bold"))
title.pack(pady=10)

tk.Label(frame, text="Enter Username:", font=("Arial", 12)).pack(pady=(10, 5))
username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
username_entry.pack()

tk.Button(frame, text="Register Fingerprint", command=register_user, font=("Arial", 11), width=25).pack(pady=10)
tk.Button(frame, text="Authenticate", command=authenticate_user, font=("Arial", 11), width=25).pack(pady=5)

root.mainloop()
