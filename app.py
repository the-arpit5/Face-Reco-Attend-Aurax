import streamlit as st
import base64
import os
from datetime import datetime
from utils.style import apply_full_page_theme, apply_custom_sidebar

# --- 1. CONFIG (STRICTLY FIRST LINE & ONLY ONCE) ---
st.set_page_config(
    page_title="Aurex Attend Pro", 
    page_icon="icon AAA.jpeg", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. APPLY GLOBAL STYLES ---
apply_full_page_theme()   # Sidebar and Page spacing fix
apply_custom_sidebar()    # Branding and Navigation links

# --- 3. IMAGE TO BASE64 HELPER ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None
    return None

logo_path = "icon AAA.jpeg"
logo_base64 = get_base64_image(logo_path)

# --- 4. DASHBOARD SPECIFIC CSS ---
st.markdown(f"""
    <style>
    /* Global App Background */
    .stApp {{ background: #050505; }}

    /* Dashboard Cards Design */
    .nav-card {{
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s ease;
        height: 170px; 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.02);
        margin-bottom: 10px;
    }}
    .nav-card:hover {{ 
        transform: translateY(-8px); 
        border-color: rgba(0, 210, 255, 0.5); 
        background: rgba(255, 255, 255, 0.05);
    }}
    
    .card-scanner {{ border-top: 4px solid #00d2ff; }}
    .card-register {{ border-top: 4px solid #92fe9d; }}
    .card-chat {{ border-top: 4px solid #ff758f; }}
    .card-records {{ border-top: 4px solid #ffd700; }}

    /* Hide default header */
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD CONTENT ---
st.markdown('<h1 style="text-align:center; color:white; font-size:45px; font-weight:900; margin-top:-30px;">AUREX DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#64748b; margin-top:-15px;'>Select a module from the sidebar or grid below</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Layout Columns
col1, col2, col3, col4 = st.columns(4)

def draw_card(column, title, icon, style, key, path):
    with column:
        st.markdown(f'''
            <div class="nav-card {style}">
                <div style="font-size:45px;">{icon}</div>
                <div style="color:white; font-weight:800; font-size:18px; margin-top:10px;">{title}</div>
            </div>
        ''', unsafe_allow_html=True)
        # Unique button keys to avoid errors
        if st.button(f"OPEN {title}", key=key, use_container_width=True):
            st.switch_page(path)

# Card Setup (Ensure these paths in 'pages/' folder are correct)
draw_card(col1, "SCANNER", "📸", "card-scanner", "btn_scan", "pages/scanner.py")
draw_card(col2, "REGISTER", "👤", "card-register", "btn_reg", "pages/ragister.py")
draw_card(col3, "CHAT", "💬", "card-chat", "btn_chat", "pages/chat.py")
draw_card(col4, "RECORDS", "📊", "card-records", "btn_rec", "pages/record.py")

st.divider()
st.markdown("<p style='text-align:center; color:#444; font-size:12px;'>Aurex Attend Pro v2.1 | Security Protocol Alpha-9</p>", unsafe_allow_html=True)
 