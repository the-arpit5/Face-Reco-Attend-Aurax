import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime

# Root directory setup
sys.path.append(os.getcwd()) 

from utils.core import load_students
from utils.style import apply_full_page_theme, apply_custom_sidebar

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Records | Aurex Pro", page_icon="", layout="wide")
apply_full_page_theme()
apply_custom_sidebar()

# --- 2. DATA LOADING ---
df_students = load_students()
today_date = datetime.now().strftime("%Y-%m-%d")
attendance_file = os.path.join("Attendance", f"Attendance_{today_date}.csv")

if os.path.exists(attendance_file):
    try:
        df_att = pd.read_csv(attendance_file)
        if not df_att.empty:
            df_att['ID'] = df_att['ID'].astype(str).str.replace('.0', '', regex=False)
    except:
        df_att = pd.DataFrame(columns=['ID', 'Name', 'Date', 'Time'])
else:
    df_att = pd.DataFrame(columns=['ID', 'Name', 'Date', 'Time'])

# --- 3. UI LAYOUT ---
st.title("📊 Records Dashboard")
st.markdown("---")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Registered", len(df_students))
m2.metric("Today's Presence", len(df_att))
m3.metric("System Status", "Operational", delta="Online")

st.write("##")

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📋 Registered Students")
    if not df_students.empty:
        df_disp = df_students.copy()
        df_disp['ID'] = df_disp['ID'].astype(str)
        st.dataframe(df_disp, use_container_width=True, hide_index=True)
    else:
        st.info("No students registered yet.")

with col_right:
    st.subheader("📝 Today's Attendance")
    
    if not df_att.empty:
        # 1. Pehle Table dikhayega
        st.dataframe(
            df_att[['ID', 'Name', 'Time']], 
            use_container_width=True, 
            hide_index=True
        )
        
        # 2. AB GREEN BOX NICHE AAYEGA (Requirement Fixed)
        st.success(f"✅ Logs for: **{today_date}**")
    else:
        st.warning(f"⚠️ No attendance records found for {today_date}.")

# --- 4. FOOTER ---
st.divider()
if st.button("🔄 Sync & Refresh Records", use_container_width=True):
    st.rerun()