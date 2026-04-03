import streamlit as st
import base64
import os

from datetime import datetime
from utils.style import apply_full_page_theme,apply_custom_sidebar

st.set_page_config(page_title="Scanner | Aurex Pro", page_icon="icon AAA.jpeg", layout="wide")
apply_full_page_theme()   # Ye purani CSS load karega
apply_custom_sidebar()    # Ye aapka naya professional sidebar load karega


# 1. Page Config
# 1. Page Config (Favicon set karne ke liye page_icon mein image ka path ya URL dein)
st.set_page_config(
    page_title="Aurex Attend Pro", 
    page_icon="icon AAA.jpeg",  # Yahan aapki photo ka path aayega
    layout="wide"
)

# --- IMAGE TO BASE64 HELPER ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

#Logo Path
logo_path = "icon AAA.jpeg"
logo_base64 = get_base64_image(logo_path)

# 2. Premium Sidebar & Dashboard CSS
st.markdown(f"""
    <style>
    /* Global App Background */
    .stApp {{ background: #050505; }}

    /* --- ULTIMATE SIDEBAR DESIGN --- */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0f172a 0%, #000000 100%) !important;
        border-right: 2px solid rgba(0, 210, 255, 0.2);
        min-width: 300px !important;
    }}

    /* Sidebar Logo Section */
    .sidebar-brand {{
        padding: 25px 15px;
        text-align: center;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px solid rgba(0, 210, 255, 0.3);
        margin: 15px;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
    }}
    
    .sidebar-brand img {{
        border-radius: 15px;
        border: 2px solid #00d2ff;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }}

    .sidebar-brand h2 {{
        color: #00d2ff;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }}

    /* Sidebar Navigation Links */
    [data-testid="stSidebarNav"] {{ padding-top: 10px; }}
    [data-testid="stSidebarNav"] ul li a {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        margin: 5px 15px !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stSidebarNav"] ul li a:hover {{
        background: rgba(0, 210, 255, 0.1) !important;
        transform: translateX(5px);
    }}

    /* --- DASHBOARD CARDS --- */
    .nav-card {{
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s ease;
        height: 160px; 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .nav-card:hover {{ transform: translateY(-8px); border-color: rgba(0, 210, 255, 0.5); }}
    .card-scanner {{ background: rgba(0, 210, 255, 0.05); border-top: 4px solid #00d2ff; }}
    .card-register {{ background: rgba(146, 254, 157, 0.05); border-top: 4px solid #92fe9d; }}
    .card-chat {{ background: rgba(255, 117, 143, 0.05); border-top: 4px solid #ff758f; }}
    .card-records {{ background: rgba(255, 215, 0, 0.05); border-top: 4px solid #ffd700; }}

    header, footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    # Custom Brand Box with your Image
    if logo_base64:
        st.markdown(f"""
            <div class="sidebar-brand">
                <img src="data:image/jpeg;base64,{logo_base64}" width="90">
                <div>
                    <h2>AUREX PRO</h2>
                    <p style="color: #64748b; font-size: 10px; margin: 0; letter-spacing: 1px;">NEXT-GEN BIOMETRICS</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback if image not found
        st.markdown('<div class="sidebar-brand"><h2>AUREX PRO</h2><p>NEXT-GEN BIOMETRICS</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Status Indicators
    st.sidebar.caption("📡 SYSTEM STATUS")
    col_s1, col_s2 = st.columns(2)
    col_s1.markdown("<p style='color:#92fe9d; font-size:12px;'>● Engine: ON</p>", unsafe_allow_html=True)
    col_s2.markdown("<p style='color:#00d2ff; font-size:12px;'>● DB: Sync</p>", unsafe_allow_html=True)
    
    st.divider()
    
    # User Profile (Mockup)
    st.markdown("""
        <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
            <p style="margin:0; font-size:12px; color:#64748b;">Logged in as:</p>
            <p style="margin:0; font-size:14px; color:white; font-weight:bold;">Admin Mode</p>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
st.markdown('<h1 style="text-align:center; color:white; font-size:45px; font-weight:900; margin-top:-50px;">AUREX DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b; margin-top:-15px;'>Select a module from the sidebar or grid below</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

def draw_card(column, title, icon, style, key, path):
    with column:
        st.markdown(f'<div class="nav-card {style}"><div style="font-size:40px;">{icon}</div><div style="color:white; font-weight:800; font-size:16px;">{title}</div></div>', unsafe_allow_html=True)
        if st.button("Access", key=key, use_container_width=True):
            st.switch_page(path)

draw_card(col1, "SCANNER", "📸", "card-scanner", "btn_scan", "pages/scanner.py")
draw_card(col2, "REGISTER", "👤", "card-register", "btn_reg", "pages/ragister.py")
draw_card(col3, "CHAT", "💬", "card-chat", "btn_chat", "pages/chat.py")
draw_card(col4, "RECORDS", "📊", "card-records", "btn_rec", "pages/record.py")

st.divider()
st.markdown("<p style='text-align:center; color:#444; font-size:12px;'>Aurex Attend Pro v2.1 | Security Protocol Alpha-9</p>", unsafe_allow_html=True)