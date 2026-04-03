import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import cv2
import os
import numpy as np
import pandas as pd
import time
import av
import mediapipe as mp
from mediapipe.python.solutions import face_mesh as mp_face_mesh
from PIL import Image
from utils.style import apply_full_page_theme, apply_custom_sidebar

# --- 1. SETUP & PATHS ---
st.set_page_config(page_title="Register | Aurex Pro", layout="wide", page_icon="👤")
apply_full_page_theme()
apply_custom_sidebar()

IMAGE_DIR = "TrainingImage"
STUDENT_DETAILS_CSV = "StudentDetails/StudentDetails.csv"
TRAINER_YML = "TrainingImageLabel/Trainner.yml" # Folder alag rakho confusion se bachne ke liye
RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

# Folders check
for folder in [IMAGE_DIR, "StudentDetails", "TrainingImageLabel"]:
    if not os.path.exists(folder): os.makedirs(folder)

# Mediapipe for Blink Detection
mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE, RIGHT_EYE = [386, 374], [159, 145]

def get_ear(landmarks, eye_indices):
    try: return abs(landmarks[eye_indices[0]].y - landmarks[eye_indices[1]].y)
    except: return 1.0

# --- 2. PROCESSOR CLASS ---
class RegistrationProcessor(VideoProcessorBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        
        self.model_loaded = os.path.exists(TRAINER_YML)
        if self.model_loaded: 
            try: self.recognizer.read(TRAINER_YML)
            except: self.model_loaded = False
        
        self.reg_id = ""
        self.reg_name = ""
        self.capture_mode = False
        self.sample_count = 0
        self.face_already_exists = False
        self.last_blink_time = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        is_blinking = False
        mesh = self.face_mesh.process(rgb_img)
        if mesh.multi_face_landmarks:
            for lm in mesh.multi_face_landmarks:
                ear = (get_ear(lm.landmark, LEFT_EYE) + get_ear(lm.landmark, RIGHT_EYE)) / 2
                if ear < 0.015: is_blinking = True

        for (x, y, w, h) in faces:
            color, label = (0, 255, 0), "READY"
            face_roi = gray[y:y+h, x:x+w]

            if self.model_loaded:
                sid, conf = self.recognizer.predict(face_roi)
                if conf < 55: # Accuracy strict rakhi hai
                    self.face_already_exists = True
                    color, label = (0, 0, 255), "🚫 ALREADY REGISTERED"
                else:
                    self.face_already_exists = False

            if self.capture_mode and not self.face_already_exists:
                if self.sample_count < 20: # 20 samples better hain
                    if is_blinking and (time.time() - self.last_blink_time > 0.4):
                        self.sample_count += 1
                        self.last_blink_time = time.time()
                        # Filename format fixed
                        img_path = f"{IMAGE_DIR}/{self.reg_name}.{self.reg_id}.{self.sample_count}.jpg"
                        cv2.imwrite(img_path, face_roi)
                    label = f"Capturing: {self.sample_count}/20"
                else:
                    self.capture_mode = False
            
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 3. UI LAYOUT ---
st.title("👤 Secure Biometric Enrollment")
st.markdown("---")

col_cam, col_input = st.columns([1.5, 1])

with col_cam:
    st.subheader("🎥 Scanner Feed")
    ctx = webrtc_streamer(
        key="registration",
        video_processor_factory=RegistrationProcessor,
        rtc_configuration=RTC_CONFIG,
        media_stream_constraints={"video": True, "audio": False}
    )
    
    is_face_known = getattr(ctx.video_processor, 'face_already_exists', False) if ctx.video_processor else False
    if is_face_known:
        st.error("🚫 Registration Blocked: Face already in database.")

with col_input:
    st.subheader("Identity Vault")
    rid = st.text_input("Assign Personal ID (Numbers only)").strip()
    rname = st.text_input("Enter Full Name").strip()

    id_taken = False
    if rid and os.path.exists(STUDENT_DETAILS_CSV):
        try:
            df_csv = pd.read_csv(STUDENT_DETAILS_CSV)
            if str(rid) in df_csv['ID'].astype(str).values:
                id_taken = True
                st.warning(f"ID {rid} is already taken.")
        except: pass

    if st.button("🚀 START SCANNING", use_container_width=True, disabled=(id_taken or is_face_known)):
        if rid.isdigit() and rname:
            if ctx.video_processor:
                ctx.video_processor.reg_id = rid
                ctx.video_processor.reg_name = rname
                ctx.video_processor.capture_mode = True
                ctx.video_processor.sample_count = 0
                st.info("Blink your eyes to capture photos!")
        else:
            st.error("Please provide valid Numeric ID and Name.")

    # --- SOLID FINALIZE LOGIC ---
    if st.button("✅ FINALIZE & LOCK", use_container_width=True):
        if not rid or not rname:
            st.error("ID and Name missing!")
        elif is_face_known:
            st.error("Face already exists!")
        else:
            # 1. Collect all images for ALL users (Not just current one)
            # Kyunki train hamesha poore dataset par karna chahiye
            faces, ids = [], []
            if os.path.exists(IMAGE_DIR):
                for f in os.listdir(IMAGE_DIR):
                    if f.endswith(".jpg"):
                        try:
                            parts = f.split(".")
                            if len(parts) >= 3:
                                user_id = int(parts[1])
                                img_path = os.path.join(IMAGE_DIR, f)
                                faces.append(np.array(Image.open(img_path).convert('L'), 'uint8'))
                                ids.append(user_id)
                        except: continue
            
            if len(faces) >= 10:
                with st.spinner("AI is creating security vault..."):
                    rec = cv2.face.LBPHFaceRecognizer_create()
                    # Zaroori: .train() use karein taaki nayi file bane
                    rec.train(faces, np.array(ids))
                    rec.save(TRAINER_YML)
                    
                    # Update CSV
                    df = pd.read_csv(STUDENT_DETAILS_CSV) if os.path.exists(STUDENT_DETAILS_CSV) else pd.DataFrame(columns=['ID', 'Name'])
                    new_row = pd.DataFrame([[rid, rname]], columns=['ID', 'Name'])
                    df = pd.concat([df, new_row]).drop_duplicates(subset=['ID'])
                    df.to_csv(STUDENT_DETAILS_CSV, index=False)
                    
                    st.success(f"🎉 Success! {rname} Registered and .yml Created!")
                    # st.balloons()
            else:
                st.error("Not enough photos found. Please capture at least 10 photos.")
