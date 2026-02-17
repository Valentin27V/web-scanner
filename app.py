import streamlit as st
import requests
from datetime import datetime

# --- 1. CONFIGURARE ---
st.set_page_config(page_title="Scanner Pro", page_icon="🛡️", layout="wide")

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- 2. BARA LATERALĂ (MENIU) ---
with st.sidebar:
    st.title("🛡️ Panou Control")
    st.info("Aplicație pentru Disertație 2026")
    st.write("---")
    show_details = st.checkbox("Arată detalii tehnice", value=True)

# --- 3. ZONA PRINCIPALĂ ---
st.title("🚀 Web Vulnerability Scanner")
st.markdown("Această aplicație analizează securitatea unui site web și generează un raport.")

url = st.text_input("URL Țintă (include https://)", "https://")
btn_scan = st.button("Lansează Scanarea", type="primary")

# --- 4. LOGICA DE SCANARE ---
if btn_scan and url:
    raport = f"RAPORT DE SECURITATE\nData: {get_time()}\nSite: {url}\n{'-'*30}\n\n"
    
    col1, col2 = st.columns(2)
    
    try:
        with st.spinner('Analizez site-ul...'):
            response = requests.get(url, timeout=5)

        # A. Verificare HTTPS
        with col1:
            st.subheader("🔒 Securitate")
            if url.startswith("https"):
                st.success("HTTPS: Activ ✅")
                raport += "[+] HTTPS: ACTIV\n"
            else:
                st.error("HTTPS: Inactiv ❌")
                raport += "[-] HTTPS: INACTIV (Critic)\n"

        # B. Verificare Server
        with col2:
            st.subheader("⚙️ Server")
            server_header = response.headers.get("Server", "Ascuns")
            st.info(f"Server detectat: {server_header}")
            raport += f"[+] Server: {server_header}\n"

        # C. Verificare Headere
        st.write("---")
        st.subheader("🛡️ Headere de Securitate")
        
        check_list = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]
        
        for item in check_list:
            if item in response.headers:
                st.success(f"{item}: Prezent ✅")
                raport += f"[+] {item}: PREZENT\n"
            else:
                st.warning(f"{item}: Lipsește ⚠️")
                raport += f"[-] {item}: LIPSEȘTE\n"

        # D. Buton Export
        st.write("---")
        st.download_button(
            label="📄 Descarcă Raportul (.txt)",
            data=raport,
            file_name="raport_scanare.txt"
        )

    except Exception as e:
        st.error(f"Eroare la conectare: {e}")