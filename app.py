import streamlit as st
import requests
import socket
import streamlit.components.v1 as components
from datetime import datetime

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(
    page_title="CyberSec Disertație",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DESIGN PERSONALIZAT (CSS) ---
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00FF41;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 0px 0px 10px #00FF41;
        margin-bottom: 20px;
    }
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #0E1117; color: #808080;
        text-align: center; padding: 10px; font-size: 12px;
        border-top: 1px solid #333; z-index: 100;
    }
    .stButton>button {
        background-color: #FF4B4B; color: white;
        border-radius: 8px; height: 50px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARA LATERALĂ (SIDEBAR) ---
with st.sidebar:
    st.markdown("## 🛡️ Panou Control")
    st.write("---")

    # === LOGO UTM ===
    try:
        st.image("https://utm.ro/wp-content/uploads/2021/01/logo-utm-simplu.png", use_column_width=True)
    except:
        st.error("Logo Error")

    # === TEXT FACULTATE ===
    st.markdown("""
        <div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
            <span style="font-size: 24px; font-weight: bold; color: white;">
                Facultatea de Informatică
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # MENIU
    choice = st.radio(
        "NAVIGARE:", 
        ["1. Scanner", "2. Laborator Atacuri", "3. Documentație"],
        index=0
    )
    
    st.write("---")
    st.info("Status: Conectat 🟢")

# --- 4. PAGINILE APLICAȚIEI ---

# === PAGINA 1: SCANNER ===
if "1. Scanner" in choice:
    st.markdown('<h1 class="main-title">SCANNER VULNERABILITĂȚI</h1>', unsafe_allow_html=True)
    st.write("---")

    col_input, col_btn = st.columns([3, 1])
    with col_input:
        url = st.text_input("Introdu URL-ul țintă:", "https://google.com")
    with col_btn:
        st.write("") 
        st.write("") 
        start_scan = st.button("🚀 SCANEAZĂ ACUM", use_container_width=True)

    if start_scan:
        with st.spinner('Analizez infrastructura țintei...'):
            st.write("---")
            c1, c2, c3 = st.columns(3)
            try:
                domain = url.replace("https://", "").replace("http://", "").split("/")[0]
                
                # C1: HTTPS
                with c1:
                    st.markdown("### 🔒 Criptare")
                    if url.startswith("https"):
                        st.success("HTTPS: ACTIV")
                    else:
                        st.error("HTTPS: INACTIV")
                
                # C2: Server (AICI ERA PROBLEMA, ACUM E REPARATĂ)
                with c2:
                    st.markdown("### 🖥️ Server")
                    try:
                        r = requests.get(url, timeout=2)
                        srv = r.headers.get("Server", "Ascuns")
                        st.info(f"Tip: {srv}")
                    except:
                        st.error("Conexiune: Fail")

                # C3: Porturi
                with c3:
                    st.markdown("### 🌐 Porturi")
                    try:
                        ports_check = [80, 443]
                        for p in ports_check:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.5)
                            res = sock.connect_ex((domain, p))
                            sock.close()
                            if res == 0:
                                st.write(f"Port {p}: **Deschis** 🔴")
                            else:
                                st.write(f"Port {p}: Închis 🟢")
                    except:
                        st.error("Eroare Porturi")
                        
            except Exception as e:
                st.error(f"Eroare generală: {e}")

# === PAGINA 2: LABORATOR ===
elif "2. Laborator" in choice:
    st.markdown('<h1 class="main-title">LABORATOR SIMULARE</h1>', unsafe_allow_html=True)
    st.warning("⚠️ ATENȚIE: Acest mediu este creat în scop educațional.")
    
    tab1, tab2 = st.tabs(["💥 SQL INJECTION", "☠️ XSS ATTACK"])

    with tab1:
        st.subheader("Simulare: Spargere Bază de Date")
        st.code("Payload: ' OR '1'='1", language="sql")
        pwd = st.text_input("Password:", type="password")
        if st.button("Încearcă Login"):
            if "' OR '1'='1" in pwd:
                st.error("ACCESS GRANTED! (SQL Injection Successful)")
            else:
                st.error("Access Denied.")

    with tab2:
        st.subheader("Simulare: Cross-Site Scripting")
        comm = st.text_input("Comentariu:")
        if st.button("Postează"):
            if "<" in comm and ">" in comm:
                st.error("XSS Detectat!")
                components.html(comm, height=50)
            else:
                st.write(comm)

# === PAGINA 3: DOCS ===
elif "3. Documentație" in choice:
    st.markdown('<h1 class="main-title">DOCUMENTAȚIE TEHNICĂ</h1>', unsafe_allow_html=True)
    st.markdown("### Arhitectura Client-Server\nFrontend: Streamlit | Backend: Python")

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        <p>Proiect Disertație 2026 | Universitatea Titu Maiorescu | Student: Valentin Staicu</p>
    </div>
    """, unsafe_allow_html=True)