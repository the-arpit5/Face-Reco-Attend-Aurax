import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import cv2
import os
import numpy as np
import av
import mediapipe as mp
import time

# Utils se functions import kar rahe hain (aapke code ke according)
from utils.core import recognize_face, mark_attendance, load_students
from utils.style import apply_full_page_theme, apply_custom_sidebar

# --- 1. SETUP ---
st.set_page_config(page_title="Scanner | Aurex Pro", page_icon="📸", layout="wide")
apply_full_page_theme()
apply_custom_sidebar()

# Mediapipe configuration for Blink Detection
mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def get_ear(landmarks, eye_indices):
    try:
        # Simple vertical distance check for blink
        p1 = landmarks[eye_indices[1]]
        p2 = landmarks[eye_indices[4]]
        return abs(p1.y - p2.y)
    except:
        return 1.0

# --- 2. SCANNER ENGINE ---
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
        self.students_df = load_students()
        self.last_blink_time = 0
        self.status_msg = ""
        self.status_type = "info" # info, success, warning

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        mesh_results = self.face_mesh.process(rgb)

        is_blinking = False
        if mesh_results.multi_face_landmarks:
            for face_lms in mesh_results.multi_face_landmarks:
                ear = (get_ear(face_lms.landmark, LEFT_EYE) + get_ear(face_lms.landmark, RIGHT_EYE)) / 2
                if ear < 0.015:  # Eye closed threshold
                    is_blinking = True

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            user_id = recognize_face(face_roi) # core.py ka function

            if user_id:
                # Student details nikaalo
                match = self.students_df[self.students_df['ID'].astype(str) == str(user_id)]
                name = match.iloc[0]['Name'] if not match.empty else "Unknown"
                
                color = (0, 255, 0) # Green for known
                label = f"{name} - BLINK TO MARK"
                
                # Agar blink kiya aur 2 second ka gap hai pichle mark se
                if is_blinking and (time.time() - self.last_blink_time > 2.0):
                    success, msg = mark_attendance(user_id, name) # core.py ka function
                    self.status_msg = msg
                    self.status_type = "success" if success else "warning"
                    self.last_blink_time = time.time()
                    color = (255, 255, 255) # White flash on success
                
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
                cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            else:
                # Unknown face
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Unknown User", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 3. UI LAYOUT ---
st.title("📸 AI Biometric Scanner")
st.markdown("<p style='color:#64748b;'>Aapki attendance tabhi lagegi jab AI aapka chehra pehchanega aur aap <b>Aankhein Jhapakayenge (Blink)</b>.</p>", unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Live Verification Feed")
    ctx = webrtc_streamer(
        key="attendance-scanner",
        video_processor_factory=VideoProcessor,
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
        media_stream_constraints={"video": True, "audio": False},
    )

with col_right:
    st.subheader("System Feedback")
    
    # Live Status showing from the Processor
    status_placeholder = st.empty()
    
    if ctx.video_processor:
        if ctx.video_processor.status_msg:
            msg = ctx.video_processor.status_msg
            if ctx.video_processor.status_type == "success":
                st.success(msg)
                # Success sound effect (Optional HTML)
                st.components.v1.html(f"<script>new Audio('https://www.soundjay.com/buttons/sounds/button-3.mp3').play();</script>", height=0)
            elif ctx.video_processor.status_type == "warning":
                st.warning(msg)
            
            # Clear message after showing
            ctx.video_processor.status_msg = ""
    
    st.info("💡 **Pro-Tip:** Agar green box aa raha hai lekin attendance nahi lag rahi, toh ek baar apni aankhein band karke kholein.")

    # Show mini records
    st.divider()
    st.caption("RECENT SCANS")
    # Yahan aap small attendance table bhi dikha sakte hain