🔐 Biometric-Based ATM Security System

🧠 About the Project
This project aims to enhance ATM security using biometric authentication. Instead of using a PIN, users register and authenticate using their fingerprint. The fingerprint data is encrypted using AES (Advanced Encryption Standard) and stored securely in a local SQLite database. The system includes a GUI for ease of use, developed with Python's tkinter.

📁 Project Structure
.
├── encryption.py            # Handles AES encryption/decryption
├── gui_app.py               # Main GUI application
├── finger_users.db          # SQLite DB storing usernames and encrypted fingerprints
├── fingerprint_samples/     # Directory to store original fingerprint images (if needed)
├── README.md                # Project README file


🚀 Installation
1. Clone the Repository
git clone https://github.com/yourusername/biometric-atm-security.git
cd biometric-atm-security

2. Install Dependencies
pip install pycryptodome pillow

3. Run the Application
python gui_app.py

▶️ Usage
1. Register a User
->Enter a username.
->Select a .png fingerprint image file.
->Click on "Register Fingerprint".

2. Authenticate a User
->Enter the registered username.
->Provide the fingerprint image again.
->Click on "Authenticate" to validate identity.

⚠️ Note: The system compares fingerprint images as binary files. For a more advanced comparison, integration with OpenCV or ML-based fingerprint matching can be implemented.
