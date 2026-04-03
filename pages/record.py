import streamlit as st
import pandas as pd
import os
from datetime import datetime
# Humne apply_record_page_style ko yahan import kiya
from utils.style import apply_full_page_theme, apply_custom_sidebar, apply_record_page_style, add_back_button

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Records | Aurex Pro", layout="wide", page_icon="📊")
apply_full_page_theme()
apply_custom_sidebar()
apply_record_page_style() # <-- CSS ab yahan se apply hogi, code clean ho gaya
add_back_button()

# --- 2. PATH SETUP ---
STUDENT_DETAILS_CSV = "StudentDetails/StudentDetails.csv"
today_date = datetime.now().strftime("%Y-%m-%d")
attendance_file = os.path.join("Attendance", f"Attendance_{today_date}.csv")

# --- 3. DATA LOADING (No Changes in Logic) ---
df_students = pd.read_csv(STUDENT_DETAILS_CSV) if os.path.exists(STUDENT_DETAILS_CSV) else pd.DataFrame()
df_attendance = pd.read_csv(attendance_file) if os.path.exists(attendance_file) else pd.DataFrame()

# Cleanup IDs taaki string mismatch na ho
for df in [df_students, df_attendance]:
    if not df.empty and 'ID' in df.columns:
        df['ID'] = df['ID'].astype(str)

# --- 4. UI HEADER ---
st.title("📊 Records Dashboard")
st.caption(f"System Operational • Logged in as Admin • {datetime.now().strftime('%A, %d %B %Y')}")
st.divider()

# --- 5. METRICS SECTION ---
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Total Registered", len(df_students))
with m2:
    st.metric("Today's Presence", len(df_attendance))

st.write("##") 

# --- 6. TABLES SECTION (Tabs for Professional Look) ---
tab1, tab2 = st.tabs(["📋 Registered Students", "📝 Today's Logs"])

with tab1:
    if not df_students.empty:
        st.dataframe(
            df_students, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn("Student ID"),
                "Name": st.column_config.TextColumn("Full Name"),
                "Date": st.column_config.DateColumn("Reg. Date"),
                "Time": st.column_config.TimeColumn("Reg. Time")
            }
        )
    else:
        st.info("No students found in the database.")

with tab2:
    if not df_attendance.empty:
        st.success(f"Showing attendance for today: {today_date}")
        st.dataframe(
            df_attendance, 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn("ID"),
                "Name": st.column_config.TextColumn("Student Name"),
                "Date": st.column_config.DateColumn("Date"),
                "Time": st.column_config.TimeColumn("Check-in Time")
            }
        )
    else:
        st.warning("No attendance records found for today.")

# --- 7. FOOTER ACTIONS ---
st.divider()
c1, c2, _ = st.columns([1,1,2])
if c1.button("🔄 Refresh Data"):
    st.rerun()

if c2.button("📥 Export Today's CSV"):
    if not df_attendance.empty:
        export_path = f"Attendance_Export_{today_date}.csv"
        df_attendance.to_csv(export_path, index=False)
        st.toast(f"File saved: {export_path}")