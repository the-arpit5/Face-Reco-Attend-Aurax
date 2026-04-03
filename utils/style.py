import streamlit as st
import os
import base64

def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""
    return ""

def apply_custom_sidebar():
    logo_path = "icon AAA.jpeg" 
    logo_base64 = get_base64_image(logo_path)

    with st.sidebar:
        if logo_base64:
            st.markdown(f"""
                <div style="text-align: center; background: rgba(255, 255, 255, 0.03); 
                            padding: 20px; border-radius: 20px; border: 1px solid rgba(0, 210, 255, 0.3); 
                            margin: 10px; box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);">
                    <img src="data:image/jpeg;base64,{logo_base64}" width="80" 
                         style="border-radius: 12px; border: 2px solid #00d2ff; margin-bottom: 10px;">
                    <h2 style="color: #00d2ff; margin: 0; font-size: 22px; font-weight: 900;">AUREX PRO</h2>
                    <p style="color: #64748b; font-size: 10px; margin: 0; letter-spacing: 1px;">NEXT-GEN BIOMETRICS</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b; font-size:12px; font-weight:bold; margin-left:5px;'>MAIN MENU</p>", unsafe_allow_html=True)
        
        st.page_link("app.py", label="DASHBOARD", icon="🏠")
        st.page_link("pages/ragister.py", label="REGISTRATION", icon="👤")
        st.page_link("pages/scanner.py", label="SCAN FACE", icon="📸")
        st.page_link("pages/record.py", label="RECORDS", icon="📊")
        st.page_link("pages/chat.py", label=" CHAT", icon="💬")
        
        st.divider()
        st.caption("📡 SYSTEM STATUS")
        col1, col2 = st.columns(2)
        col1.markdown("<p style='color:#92fe9d; font-size:12px;'>● Engine: ON</p>", unsafe_allow_html=True)
        col2.markdown("<p style='color:#00d2ff; font-size:12px;'>● DB: Sync</p>", unsafe_allow_html=True)

# 1. DASHBOARD KE LIYE (Pure Black BG + Gradient Sidebar)
def apply_full_page_theme():
    st.markdown("""
        <style>
        /* Main Page Background */
        .stApp { background: #050505 !important; }
        
        /* Sidebar Design */
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            background: linear-gradient(180deg, #0f172a 0%, #000000 100%) !important;
            border-right: 1px solid rgba(0, 210, 255, 0.2);
        }
        
        /* Hide Header */
        header { visibility: hidden !important; }
        
        /* Navigation Button Styles */
        .stPageLink button {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 10px !important;
            color: white !important;
            margin-bottom: 5px !important;
            transition: 0.3s;
        }
        .stPageLink button:hover {
            border: 1px solid #00d2ff !important;
            background: rgba(0, 210, 255, 0.1) !important;
            transform: translateX(5px);
        }
        </style>
    """, unsafe_allow_html=True)

# 2. BAAKI PAGES KE LIYE (BG matches Sidebar Gradient)
# 2. BAAKI PAGES KE LIYE (BG matches Sidebar Gradient)
# 2. BAAKI PAGES KE LIYE (Modern Separation Look)
def apply_inner_page_theme():
    st.markdown("""
        <style>
        /* 1. Main Page Background (Thoda light blue-black gradient taaki content utha hua dikhe) */
        .stApp { 
            background: radial-gradient(circle at top right, #1e293b 0%, #050505 100%) !important;
            background-attachment: fixed !important;
        }
        
        <style>
        /* 1. Poore page ka background gradient */
        .stApp { 
            background: linear-gradient(180deg, #0f172a 0%, #000000 100%) !important; 
            background-attachment: fixed !important;
        }
        
        /* 2. Sidebar ko solid dark banaya (Dashboard jaisa) */
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            /* Yahan 0.5 ki jagah solid color use kiya hai */
            background-color: #050505 !important; 
            background-image: linear-gradient(180deg, #0f172a 0%, #000000 100%) !important;
            border-right: 1px solid rgba(0, 210, 255, 0.2) !important;
        }

        /* Hover Effect: Glow and Slide */
        .stPageLink button:hover {
            border: 1px solid #00d2ff !important;
            background: rgba(0, 210, 255, 0.15) !important;
            color: #ffffff !important;
            transform: translateX(8px);
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
        }

        /* 4. Content Area Settings */
        header { visibility: hidden !important; }
        
        /* Elements color fix */
        h1, h2, h3, p {
            color: #f8fafc !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

def add_back_button():
    col1, _ = st.columns([1, 4])
    with col1:
        st.page_link("app.py", label="BACK", icon="⬅️")
    st.markdown("---")

def apply_record_page_style():
    st.markdown("""
        <style>
        div[data-testid="stMetric"] {
            background-color: rgba(14, 17, 23, 0.8) !important; 
            border: 1px solid #1f2937 !important;
            padding: 10px !important;
            border-radius: 8px !important;
        }
        </style>
    """, unsafe_allow_html=True)