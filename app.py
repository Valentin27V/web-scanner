import streamlit as st
import requests
import socket
import streamlit.components.v1 as components
from datetime import datetime
from urllib.parse import urlparse

# --- CONFIGURARE ---
st.set_page_config(page_title="CyberSec Disertație", page_icon="🛡️", layout="wide")

# CSS Custom
st.markdown("""
    <style>
    .main-header {font-size: 24px; font-weight: bold; color: #4CAF50;}
    .vuln-box {border: 1px solid #ff4b4b; padding: 15px; border-radius: 5px; margin-bottom: 10px;}
    /* Facem butoanele din meniu să arate mai bine */
    .stRadio > label {font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# --- MENIU DE NAVIGARE (TOATE OPȚIUNILE VIZIBILE) ---
with st.sidebar:
    st.title("🛡️ Panou Control")
    st.image("https://cdn-icons-png.flaticon.com/512/9662/9662366.png", width=100)
    st.write("---")
    st.write("📂 **Navigare Proiect:**")
    
    # Aici e modificarea: Folosim 'radio' în loc de 'selectbox'
    choice = st.radio(
        "Alege Modulul:", 
        ["1. Scanner Vulnerabilități", "2. Laborator Atacuri (Simulare)", "3. Teorie & Documentație"],
        index=0 # Pornește implicit pe prima opțiune
    )
    
    st.write("---")
    st.info("Status: Conectat ✅\nVersiune: 3.1 Final")

# ==========================================
# PAGINA 1: SCANNER (Ce aveam deja)
# ==========================================
if choice == "1. Scanner Vulnerabilități":
    st.title("🕵️ Scanner de Vulnerabilități Web")
    st.markdown("Instrument automatizat pentru identificarea problemelor de securitate.")

    url = st.text_input("URL Țintă:", "https://google.com")
    
    col1, col2 = st.columns(2)
    with col1:
        scan_ports_opt = st.checkbox("Scanare Porturi (Active)", value=True)
    with col2:
        st.write("Opțiuni Avansate:")
        st.info("Analiza HTTPS este activă implicit.")

    if st.button("🚀 PORNEȘTE SCANAREA", type="primary"):
        st.write("---")
        
        # 1. HTTPS CHECK
        try:
            response = requests.get(url, timeout=3)
            if url.startswith("https"):
                st.success("✅ Conexiune Securizată (HTTPS)")
            else:
                st.error("❌ Conexiune Nesecurizată (HTTP) - Risc de 'Man-in-the-Middle'")
                
            # 2. HEADERS CHECK
            st.subheader("🛡️ Analiză Headere")
            headers = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]
            for h in headers:
                if h in response.headers:
                    st.success(f"✅ {h}: Prezent")
                else:
                    st.warning(f"⚠️ {h}: Lipsește")

        except:
            st.error("Nu s-a putut conecta la site.")

        # 3. PORT SCANNER SIMPLU
        if scan_ports_opt:
            st.subheader("🌐 Scanare Porturi")
            domain = url.replace("https://", "").replace("http://", "").split("/")[0]
            ports = {80: "HTTP", 443: "HTTPS", 21: "FTP", 22: "SSH"}
            
            for port, name in ports.items():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((domain, port))
                if result == 0:
                    st.error(f"🔴 Port {port} ({name}) este DESCHIS")
                else:
                    st.success(f"🟢 Port {port} ({name}) este închis")
                sock.close()

# ==========================================
# PAGINA 2: LABORATOR ATACURI
# ==========================================
elif choice == "2. Laborator Atacuri (Simulare)":
    st.title("🧪 Laborator de Simulare Atacuri")
    st.info("Această secțiune demonstrează practic vulnerabilitățile menționate în disertație.")

    tab1, tab2, tab3 = st.tabs(["SQL Injection", "XSS (Cross-Site Scripting)", "Command Injection"])

    # --- SCENARIU 1: SQL INJECTION ---
    with tab1:
        st.header("1. SQL Injection (SQLi)")
        st.markdown("""
        **Descriere:** Atacatorul manipulează interogarea SQL pentru a ocoli autentificarea.
        **Payload Clasic:** `' OR '1'='1`
        """)
        
        st.markdown("### 🔐 Formular Login Vulnerabil")
        username = st.text_input("Utilizator:", placeholder="admin")
        password = st.text_input("Parolă:", type="password", placeholder="Încearcă: ' OR '1'='1")
        
        if st.button("Autentificare (Simulare)"):
            if password == "admin123":
                st.success("Autentificare reușită (Normal).")
            elif "' OR '1'='1" in password or '" OR "1"="1' in password:
                st.error("⚠️ ATAC REUȘIT! SQL Injection detectat.")
                st.success("🔓 Sistemul a fost păcălit! Ai primit acces de Administrator.")
                st.code(f"SELECT * FROM users WHERE user='{username}' AND pass='{password}'", language="sql")
                st.write("Deoarece '1'='1' este mereu adevărat, baza de date a returnat 'TRUE'.")
            else:
                st.error("Parolă greșită.")

    # --- SCENARIU 2: XSS ---
    with tab2:
        st.header("2. XSS (Cross-Site Scripting)")
        st.markdown("""
        **Descriere:** Atacatorul injectează cod JavaScript malițios.
        **Payload:** `<script>alert('Hacked')</script>` sau `<h1>HACKED</h1>`
        """)
        
        st.markdown("### 💬 Comentarii Vulnerabile")
        user_input = st.text_area("Scrie un comentariu:", placeholder="Scrie ceva sau pune cod HTML...")
        
        if st.button("Postează Comentariul"):
            st.write("Previzualizare (Vulnerabil):")
            components.html(user_input, height=100, scrolling=True)
            if "<script>" in user_input or "<h" in user_input:
                st.error("⚠️ XSS POSIBIL! Codul HTML/JS a fost executat.")

    # --- SCENARIU 3: COMMAND INJECTION ---
    with tab3:
        st.header("3. Command Execution (RCE)")
        st.markdown("""
        **Descriere:** Atacatorul execută comenzi de sistem.
        **Payload:** `127.0.0.1; ls`
        """)
        
        target_ip = st.text_input("Ping IP:", "8.8.8.8")
        
        if st.button("Execută Ping"):
            if ";" in target_ip or "&&" in target_ip:
                st.error("⚠️ Command Injection Detectat!")
                st.code(f"ping -c 1 {target_ip}", language="bash")
                st.write("Sistemul ar fi executat comanda de după ';'.")
            else:
                st.info(f"Pinging {target_ip}...")
                st.success("Ping reușit (Safe).")

# ==========================================
# PAGINA 3: DOCUMENTAȚIE
# ==========================================
elif choice == "3. Teorie & Documentație":
    st.title("📚 Documentație Tehnică")
    st.markdown("### Componentele Aplicației Web")
    st.write("- **Frontend:** Streamlit")
    st.write("- **Backend:** Python")
    st.write("- **Rețea:** Socket & Requests")
    
    st.markdown("### Măsuri de Securizare")
    st.info("1. Input Validation\n2. Prepared Statements\n3. WAF (Web Application Firewall)")