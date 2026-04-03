import streamlit as st
import pandas as pd
import os
import sys
from utils.style import apply_full_page_theme,apply_custom_sidebar

st.set_page_config(page_title="Scanner | Aurex Pro", page_icon="icon AA.jpeg", layout="wide")
apply_full_page_theme()   # Ye purani CSS load karega
apply_custom_sidebar()    # Ye aapka naya professional sidebar load karega


# ==========================================
# --- 🛠️ STEP 1: PATH FIX (MASTER) ---
# ==========================================
# Ye current file (pages/chat.py) se root (attendance) folder dhoondhega
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ==========================================
# --- 🛠️ STEP 2: TRY IMPORTS ---
# ==========================================
try:
    from utils.core import load_students
    from utils.style import apply_full_page_theme
except ImportError:
    st.error("❌ 'utils' folder nahi mil raha! 'core.py' ka naam check karein.")
    st.stop()

# ==========================================
# --- 🛠️ STEP 3: PAGE SETUP ---
# ==========================================
st.set_page_config(page_title="Student Chat Lounge", layout="wide")
apply_full_page_theme()

# 2. Session State Initialization
if "login" not in st.session_state:
    st.session_state.login = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "messages" not in st.session_state:
    st.session_state.messages = [] 

# --- LOGIN LOGIC ---
if not st.session_state.login:
    st.markdown('<h1 style="text-align:center;"> Student Login</h1>', unsafe_allow_html=True)
    st.info("Chat lounge mein jaane ke liye login karein.")
    
    # Utils.core se students load ho rahe hain
    df = load_students() 
    
    with st.container(border=True):
        u_name = st.text_input("Registered Name")
        u_id = st.text_input("Student ID")
        
        if st.button("Login & Enter", use_container_width=True):
            if not df.empty:
                # Name aur ID matching logic (Safe string comparison)
                user_match = df[(df["Name"].str.lower() == u_name.lower().strip()) & 
                                (df["ID"].astype(str) == str(u_id).strip())]
                
                if not user_match.empty:
                    st.session_state.login = True
                    st.session_state.user = user_match.iloc[0]["Name"]
                    st.rerun() 
                else:
                    st.error("❌ Details match nahi hui! Pehle Register karein.")
            else:
                st.warning("⚠️ Database khali hai. Pehle student register karein.")

# --- PROFESSIONAL CHAT INTERFACE ---
else:
    # Sidebar for logout
    with st.sidebar:
        st.markdown(f'<div style="text-align:center;"><h2>👤 Profile</h2><p>Welcome, <b>{st.session_state.user}</b></p></div>', unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.login = False
            st.session_state.user = ""
            st.session_state.messages = [] 
            st.rerun()

    st.title("💬 Student Chat Lounge")
    st.caption("Aapka safe communication space.")

    # Display Chat History
    for msg in st.session_state.messages:
        role = "user" if msg["name"] == st.session_state.user else "assistant"
        avatar = "👤" if role == "user" else "🎓"
        
        with st.chat_message(role, avatar=avatar):
            st.markdown(f"**{msg['name']}**")
            st.write(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Apna message yahan likhein..."):
        # Message ko session mein save karna
        st.session_state.messages.append({
            "name": st.session_state.user,
            "content": prompt
        })
        # Turant dikhane ke liye rerun
        st.rerun()