1	import streamlit as st
2	import base64
3	import os
4	# Naya Code (Cloud Friendly)
5	from mediapipe.python.solutions import face_mesh as mp_face_mesh
6	face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
7	
8	from datetime import datetime
9	from utils.style import apply_full_page_theme,apply_custom_sidebar
10	
11	st.set_page_config(page_title="Scanner | Aurex Pro", page_icon="icon AAA.jpeg", layout="wide")
12	apply_full_page_theme()   # Ye purani CSS load karega
13	apply_custom_sidebar()    # Ye aapka naya professional sidebar load karega
14	
15	# 1. Page Config
16	# 1. Page Config (Favicon set karne ke liye page_icon mein image ka path ya URL dein)
17	st.set_page_config(
18	    page_title="Aurex Attend Pro", 
19	    page_icon="icon AAA.jpeg",  # Yahan aapki photo ka path aayega
20	    layout="wide"
21	)
22	
23	# --- IMAGE TO BASE64 HELPER ---
24	def get_base64_image(image_path):
25	    try:
26	        with open(image_path, "rb") as img_file:
27	            return base64.b64encode(img_file.read()).decode()
28	    except Exception as e:
29	        return None
30	
31	#Logo Path
32	logo_path = "icon AAA.jpeg"
33	logo_base64 = get_base64_image(logo_path)
34	
35	# 2. Premium Sidebar & Dashboard CSS
36	st.markdown(f"""
37	    <style>
38	    /* Global App Background */
39	    .stApp {{ background: #050505; }}
40	
41	    /* --- ULTIMATE SIDEBAR DESIGN --- */
42	    [data-testid="stSidebar"] {{
43	        background: linear-gradient(180deg, #0f172a 0%, #000000 100%) !important;
44	        border-right: 2px solid rgba(0, 210, 255, 0.2);
45	        min-width: 300px !important;
46	    }}
47	
48	    /* Sidebar Logo Section */
49	    .sidebar-brand {{
50	        padding: 25px 15px;
51	        text-align: center;
52	        background: rgba(255, 255, 255, 0.03);
53	        border-radius: 20px;
54	        border: 1px solid rgba(0, 210, 255, 0.3);
55	        margin: 15px;
56	        box-shadow: 0 0 20px rgba(0, 210, 255, 0.1);
57	        display: flex;
58	        flex-direction: column;
59	        align-items: center;
60	        gap: 12px;
61	    }}
62	    
63	    .sidebar-brand img {{
64	        border-radius: 15px;
65	        border: 2px solid #00d2ff;
66	        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
67	    }}
68	
69	    .sidebar-brand h2 {{
70	        color: #00d2ff;
71	        font-size: 24px;
72	        font-weight: 900;
73	        letter-spacing: 2px;
74	        margin: 0;
75	        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
76	    }}
77	
78	    /* Sidebar Navigation Links */
79	    [data-testid="stSidebarNav"] {{ padding-top: 10px; }}
80	    [data-testid="stSidebarNav"] ul li a {{
81	        background: rgba(255, 255, 255, 0.03) !important;
82	        border-radius: 12px !important;
83	        margin: 5px 15px !important;
84	        padding: 10px !important;
85	        transition: all 0.3s ease !important;
86	    }}
87	    [data-testid="stSidebarNav"] ul li a:hover {{
88	        background: rgba(0, 210, 255, 0.1) !important;
89	        transform: translateX(5px);
90	    }}
91	
92	    /* --- DASHBOARD CARDS --- */
93	    .nav-card {{
94	        backdrop-filter: blur(15px);
95	        border-radius: 20px;
96	        padding: 20px;
97	        text-align: center;
98	        transition: all 0.4s ease;
99	        height: 160px; 
100	        display: flex;
101	        flex-direction: column;
102	        align-items: center;
103	        justify-content: center;
104	        border: 1px solid rgba(255, 255, 255, 0.08);
105	    }}
106	    .nav-card:hover {{ transform: translateY(-8px); border-color: rgba(0, 210, 255, 0.5); }}
107	    .card-scanner {{ background: rgba(0, 210, 255, 0.05); border-top: 4px solid #00d2ff; }}
108	    .card-register {{ background: rgba(146, 254, 157, 0.05); border-top: 4px solid #92fe9d; }}
109	    .card-chat {{ background: rgba(255, 117, 143, 0.05); border-top: 4px solid #ff758f; }}
110	    .card-records {{ background: rgba(255, 215, 0, 0.05); border-top: 4px solid #ffd700; }}
111	
112	    header, footer {{visibility: hidden;}}
113	    </style>
114	    """, unsafe_allow_html=True)
115	
116	# --- SIDEBAR CONTENT ---
117	with st.sidebar:
118	    # Custom Brand Box with your Image
119	    if logo_base64:
120	        st.markdown(f"""
121	            <div class="sidebar-brand">
122	                <img src="data:image/jpeg;base64,{logo_base64}" width="90">
123	                <div>
124	                    <h2>AUREX PRO</h2>
125	                    <p style="color: #64748b; font-size: 10px; margin: 0; letter-spacing: 1px;">NEXT-GEN BIOMETRICS</p>
126	                </div>
127	            </div>
128	        """, unsafe_allow_html=True)
129	    else:
130	        # Fallback if image not found
131	        st.markdown('<div class="sidebar-brand"><h2>AUREX PRO</h2><p>NEXT-GEN BIOMETRICS</p></div>', unsafe_allow_html=True)
132	    
133	    st.markdown("<br>", unsafe_allow_html=True)
134	    
135	    # Status Indicators
136	    st.sidebar.caption("📡 SYSTEM STATUS")
137	    col_s1, col_s2 = st.columns(2)
138	    col_s1.markdown("<p style='color:#92fe9d; font-size:12px;'>● Engine: ON</p>", unsafe_allow_html=True)
139	    col_s2.markdown("<p style='color:#00d2ff; font-size:12px;'>● DB: Sync</p>", unsafe_allow_html=True)
140	    
141	    st.divider()
142	    
143	    # User Profile (Mockup)
144	    st.markdown("""
145	        <div style="padding: 10px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
146	            <p style="margin:0; font-size:12px; color:#64748b;">Logged in as:</p>
147	            <p style="margin:0; font-size:14px; color:white; font-weight:bold;">Admin Mode</p>
148	        </div>
149	    """, unsafe_allow_html=True)
150	
151	# --- MAIN DASHBOARD ---
152	st.markdown('<h1 style="text-align:center; color:white; font-size:45px; font-weight:900; margin-top:-50px;">AUREX DASHBOARD</h1>', unsafe_allow_html=True)
153	st.markdown("<p style='text-align:center; color:#64748b; margin-top:-15px;'>Select a module from the sidebar or grid below</p>", unsafe_allow_html=True)
154	st.markdown("<br>", unsafe_allow_html=True)
155	
156	col1, col2, col3, col4 = st.columns(4)
157	
158	def draw_card(column, title, icon, style, key, path):
159	    with column:
160	        st.markdown(f'<div class="nav-card {style}"><div style="font-size:40px;">{icon}</div><div style="color:white; font-weight:800; font-size:16px;">{title}</div></div>', unsafe_allow_html=True)
161	        if st.button("Access", key=key, use_container_width=True):
162	            st.switch_page(path)
163	
164	draw_card(col1, "SCANNER", "📸", "card-scanner", "btn_scan", "pages/scanner.py")
165	draw_card(col2, "REGISTER", "👤", "card-register", "btn_reg", "pages/ragister.py")
166	draw_card(col3, "CHAT", "💬", "card-chat", "btn_chat", "pages/chat.py")
167	draw_card(col4, "RECORDS", "📊", "card-records", "btn_rec", "pages/record.py")
168	
169	st.divider()
170	st.markdown("<p style='text-align:center; color:#444; font-size:12px;'>Aurex Attend Pro v2.1 | Security Protocol Alpha-9</p>", unsafe_allow_html=True)


