import streamlit as st
import os
import base64

def apply_custom_sidebar():
    # 1. Logo Path (Ensure file name is correct in your folder)
    logo_path = "icon AAA.jpeg" 
    
    # 2. Image to Base64 (Sidebar Branding ke liye)
    logo_base64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()

    with st.sidebar:
        # --- BRANDING BOX ---
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

        # --- CUSTOM NAVIGATION (Uniform size for all pages) ---
        st.markdown("<p style='color:#64748b; font-size:12px; font-weight:bold; margin-left:5px;'>MAIN MENU</p>", unsafe_allow_html=True)
        
        st.page_link("app.py", label="DASHBOARD", icon="🏠")
        st.page_link("pages/ragister.py", label="REGISTRATION", icon="👤")
        st.page_link("pages/scanner.py", label="SCAN FACE", icon="📸")
        st.page_link("pages/record.py", label="RECORDS", icon="📊")
        st.page_link("pages/chat.py", label=" CHAT", icon="💬")
        
        st.divider()
        
        # --- SYSTEM STATUS ---
        st.caption("📡 SYSTEM STATUS")
        col1, col2 = st.columns(2)
        col1.markdown("<p style='color:#92fe9d; font-size:12px;'>● Engine: ON</p>", unsafe_allow_html=True)
        col2.markdown("<p style='color:#00d2ff; font-size:12px;'>● DB: Sync</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # --- ADMIN INFO ---
        st.markdown("""
            <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <p style="margin:0; font-size:11px; color:#64748b;">Current Session:</p>
                <p style="margin:0; font-size:13px; color:white; font-weight:bold;">Admin Mode</p>
            </div>
        """, unsafe_allow_html=True)

def apply_full_page_theme():
    # Logo for Mobile Corner
    logo_path = "icon AAA.jpeg" 
    logo_base_64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base_64 = base64.b64encode(img_file.read()).decode()

    # CSS for Sidebar Fix and Mobile Icon
    st.markdown(f"""
        <style>
        /* 1. Sidebar Width Constant (Sabhi pages par same rahega) */
        [data-testid="stSidebar"] {{
            min-width: 300px !important;
            max-width: 300px !important;
            background: linear-gradient(180deg, #0f172a 0%, #000000 100%) !important;
        }}
        
        [data-testid="stSidebarNav"] {{ display: none; }}

        /* 2. Mobile Header Logo (Sirf Phone par dikhega) */
        @media (max-width: 1023px) {{
            .mobile-top-logo {{
                position: fixed;
                top: 10px;
                right: 55px; 
                z-index: 999999;
                border: 1px solid #00d2ff;
                border-radius: 8px;
                width: 32px;
                height: 32px;
            }}
        }}
        @media (min-width: 1024px) {{
            .mobile-top-logo {{ display: none; }}
        }}

        /* 3. Navigation Buttons Styling */
        .stPageLink button {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid transparent !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
            padding: 10px !important;
            width: 100% !important;
        }}
        .stPageLink button:hover {{
            background: rgba(0, 210, 255, 0.1) !important;
            border: 1px solid rgba(0, 210, 255, 0.4) !important;
            transform: translateX(5px);
        }}
        </style>
        <img class="mobile-top-logo" src="data:image/jpeg;base64,{logo_base_64}">
    """, unsafe_allow_html=True)

def apply_record_page_style():
    st.markdown("""
        <style>
        /* Common Metric Style */
        div[data-testid="stMetric"] {
            background-color: #0e1117 !important; 
            border: 1px solid #1f2937 !important;
            border-radius: 8px !important;
        }

        /* --- LAPTOP VIEW (Tight Professional Layout) --- */
        @media (min-width: 1024px) {
            div[data-testid="stMetric"] {
                padding: 5px 12px !important;
                max-width: 160px !important; 
            }
            [data-testid="column"] {
                width: fit-content !important;
                flex: unset !important;
                min-width: 150px !important;
            }
            [data-testid="stVerticalBlock"] > div {
                padding-bottom: 0px !important;
                margin-bottom: -10px !important;
            }
            .stTabs {
                margin-top: -50px !important; 
            }
            h1 { margin-bottom: -20px !important; }
        }

        /* --- MOBILE VIEW (Phone optimized) --- */
        @media (max-width: 1023px) {
            div[data-testid="stMetric"] {
                padding: 10px !important;
                margin-bottom: 5px !important;
            }
            [data-testid="column"] {
                width: 48% !important; /* 2 boxes per row */
                flex: 1 1 45% !important;
            }
            .stTabs { margin-top: 0px !important; }
            [data-testid="stMetricValue"] {
                font-size: 1.2rem !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def add_back_button():
    col1, _ = st.columns([1, 4])
    with col1:
        # Ye button har page se Dashboard (app.py) par le jayega
        if st.page_link("app.py", label="BACK", icon="⬅️"):
            pass 
    st.markdown("---")