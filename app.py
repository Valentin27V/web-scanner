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
    /* Titluri */
    .main-title {
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
        color: #00FF41;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 0px 0px 10px #00FF41;
        margin-bottom: 20px;
    }
    /* Carduri */
    .css-1r6slb0 {
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        background-color: #0E1117;
    }
    /* Footer */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #0E1117; color: #808080;
        text-align: center; padding: 10px; font-size: 12px;
        border-top: 1px solid #333; z-index: 100;
    }
    /* Butoane */
    .stButton>button {
        background-color: #FF4B4B; color: white;
        border-radius: 8px; height: 50px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BARA LATERALĂ (SIDEBAR) - ACTUALIZATĂ ---
with st.sidebar:
    st.markdown("## 🛡️ Panou Control")
    st.write("---")

    # LOGO UTM
    try:
        st.image("https://utm.ro/wp-content/uploads/2021/01/logo-utm-simplu.png", use_column_width=True)
    except:
        st.error("Logo-ul nu s-a putut încărca.")

    # TEXT FACULTATE (Bold 24)
    st.markdown("""
        <div style="text-align: center; margin-top: 10px; margin-bottom: 20px;">
            <span style="font-size: 24px; font-weight: bold;">
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
    st.markdown("<p style='text-align: center;'>Analizează securitatea serverelor web în timp real.</p>", unsafe_allow_html=True)
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
                
                with c1:
                    st.markdown("### 🔒 Criptare")
                    if url.startswith("https"):
                        st.success("HTTPS: ACTIV")
                        st.metric("Certificat", "Valid")
                    else:
                        st.error("HTTPS: INACTIV")
                        st.metric("Certificat", "Lipsă")
                
                with c2:
                    st.markdown("### 🖥️ Server")
                    try:
                        r = requests.get(url, timeout=2)