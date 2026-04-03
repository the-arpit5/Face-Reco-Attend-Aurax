import cv2
import os
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime

# --- 🛠️ Path Setup ---
FILE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BASE_DIR = os.path.dirname(FILE_DIR) 

DATA_FILE = os.path.join(BASE_DIR, "StudentDetails", "StudentDetails.csv")
TRAINER_FILE = os.path.join(BASE_DIR, "TrainingImageLabel", "Trainner.yml")
IMAGE_DIR = os.path.join(BASE_DIR, "TrainingImage")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "Attendance")

# Ensure folders exist
for folder in [os.path.dirname(DATA_FILE), os.path.dirname(TRAINER_FILE), IMAGE_DIR, ATTENDANCE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# 1. CHECK IF FACE ALREADY EXISTS (Registration Time)
def is_face_registered(face_gray):
    if not os.path.exists(TRAINER_FILE):
        return False, None
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read(TRAINER_FILE)
        user_id, confidence = recognizer.predict(face_gray)
        # Registration ke waqt strict check
        if confidence < 50: 
            return True, user_id
    except:
        pass
    return False, None

# 2. SAVE STUDENT DETAILS
def save_student(id, name):
    try:
        if not str(id).strip() or not str(name).strip():
            return False, "Error: ID and Name are required!"

        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
        else:
            df = pd.DataFrame(columns=['ID', 'Name', 'Date', 'Time'])
        
        df['ID'] = df['ID'].astype(str)
        if str(id) in df['ID'].values:
            return False, f"ID {id} is already in our records!"

        new_entry = {
            "ID": str(id), 
            "Name": name, 
            "Date": datetime.now().strftime("%Y-%m-%d"), 
            "Time": datetime.now().strftime("%H:%M:%S")
        }
        
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        return True, f"Success: {name} registered!"
    except Exception as e:
        return False, f"Database Error: {str(e)}"

# 3. TRAIN THE MODEL
def train_model():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        if not os.path.exists(IMAGE_DIR) or not os.listdir(IMAGE_DIR):
            return False, "No images found for training!"

        image_paths = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")]
        
        face_samples, ids = [], []
        for path in image_paths:
            img = np.array(Image.open(path).convert('L'), 'uint8')
            try:
                # Filename format: Name.ID.Count.jpg
                user_id = int(os.path.split(path)[-1].split(".")[1])
                faces = detector.detectMultiScale(img)
                for (x, y, w, h) in faces:
                    face_samples.append(img[y:y+h, x:x+w])
                    ids.append(user_id)
            except:
                continue 

        if not face_samples: return False, "No valid faces found!"
        
        recognizer.train(face_samples, np.array(ids))
        recognizer.save(TRAINER_FILE)
        return True, "AI Model Trained Successfully!"
    except Exception as e:
        return False, f"Training Error: {str(e)}"

# 4. RECOGNIZE FACE (Accuracy Fix Applied)
def recognize_face(face_roi):
    if not os.path.exists(TRAINER_FILE): 
        return None
        
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(TRAINER_FILE)
        user_id, confidence = recognizer.predict(face_roi)
        
        # NOTE: Confidence jitna kam (low), accuracy utni zyada (high)
        # 50-55 is best for similar faces (like family members)
        if confidence < 55: 
            return user_id
        else:
            return None # Match nahi mila toh Unknown
    except:
        return None

# 5. MARK ATTENDANCE
def mark_attendance(id, name):
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(ATTENDANCE_DIR, f"Attendance_{today}.csv")
        
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=['ID', 'Name', 'Date', 'Time'])

        df['ID'] = df['ID'].astype(str)
        if str(id) in df['ID'].values:
            return False, f"{name}, already marked for today!"

        new_row = {
            "ID": str(id), 
            "Name": name, 
            "Date": today, 
            "Time": datetime.now().strftime("%H:%M:%S")
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(filename, index=False)
        return True, f"Success: {name} marked present."
    except Exception as e:
        return False, f"File Error: {str(e)}"

# 6. LOAD STUDENTS
def load_students():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df['ID'] = df['ID'].astype(str)
            return df.dropna(subset=['ID', 'Name'])
        except:
            return pd.DataFrame(columns=['ID', 'Name'])
    return pd.DataFrame(columns=['ID', 'Name'])