# encryption.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

KEY = hashlib.sha256(b"your_secret_key_here").digest() 

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt(data):
    data = pad(data)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(data)
    return base64.b64encode(iv + encrypted).decode('utf-8')

def decrypt(enc_data):
    enc = base64.b64decode(enc_data)
    iv = enc[:AES.block_size]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(enc[AES.block_size:])
    return decrypted.rstrip(b"\0")