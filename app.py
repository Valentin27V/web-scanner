import streamlit as st
import requests
import socket
from datetime import datetime
from urllib.parse import urlparse

# --- 1. CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="CyberScanner Pro", page_icon="🛡️", layout="wide")

# CSS pentru stilizare (facem titlurile colorate)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
    .report-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNCȚII DE SECURITATE ---

def get_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return url

def scan_ports(target_host):
    # Porturi comune de verificat
    ports = {
        21: "FTP (Transfer Fișiere)",
        22: "SSH (Admin Access)",
        80: "HTTP (Web)",
        443: "HTTPS (Web Securizat)",
        3306: "MySQL (Bază de date)",
        8080: "Alt Web Server"
    }
    
    results = {}
    
    # Bara de progres pentru porturi
    progress_text = "Scanare porturi în curs..."
    my_bar = st.progress(0, text=progress_text)
    
    for i, (port, service) in enumerate(ports.items()):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # Așteptăm maxim 1 secundă per port
        result = sock.connect_ex((target_host, port))
        if result == 0:
            results[port] = (service, "DESCHIS ⚠️")
        else:
            results[port] = (service, "Închis")
        sock.close()
        # Actualizăm bara de progres
        my_bar.progress((i + 1) / len(ports), text=f"Verific portul {port}...")
    
    my_bar.empty() # Ștergem bara la final
    return results

def check_sql_injection(url):
    # Testăm dacă URL-ul răspunde ciudat la caractere speciale
    payloads = ["'", "\"", " OR 1=1", "--"]
    vulnerabilities = []
    
    try:
        original_response = requests.get(url, timeout=3)
        for payload in payloads:
            test_url = f"{url}{payload}"
            response = requests.get(test_url, timeout=3)
            
            # Dacă site-ul își schimbă drastic lungimea sau dă eroare de SQL
            if "SQL syntax" in response.text or "mysql_" in response.text:
                vulnerabilities.append(f"Posibil vulnerabil la payload: {payload}")
            elif len(response.text) != len(original_response.text):
                # Aceasta e o verificare simplistă, dar utilă pentru demo
                pass 
    except:
        return ["Nu s-a putut testa SQL Injection (Conexiune refuzată)"]
        
    if not vulnerabilities:
        return ["Nu s-au detectat vulnerabilități evidente la SQLi simplu."]
    return vulnerabilities

# --- 3. INTERFAȚA GRAFICĂ (UI) ---

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2716/2716612.png", width=80)
    st.title("🛡️ Panou Control")
    st.info("Versiunea 3.0 - Disertație")
    st.markdown("---")
    st.write("🔧 **Module Active:**")
    st.checkbox("Scanare HTTPS & Headere", value=True, disabled=True)
    scan_p = st.checkbox("Scanare Porturi (Lent)", value=True)
    scan_sql = st.checkbox("Test SQL Injection", value=True)

# Main Area
st.title("🕵️ CyberScanner 3.0")
st.markdown("Un scanner avansat pentru detectarea vulnerabilităților web.")

col1, col2 = st.columns([3, 1])
with col1:
    url = st.text_input("Țintă (URL):", "https://google.com")
with col2:
    st.write("") # Spațiu gol pentru aliniere
    st.write("")
    btn_start = st.button("🚀 SCANEAZĂ")

# --- 4. LOGICA PRINCIPALĂ ---

if btn_start and url:
    st.write("---")
    raport_final = f"RAPORT FINAL DE SECURITATE\nData: {datetime.now()}\nȚinta: {url}\n\n"
    
    # A. Extragere domeniu
    domain = get_domain(url)
    st.subheader(f"🔍 Analiză pentru: {domain}")
    
    # 1. HEADERE & HTTPS
    with st.expander("1. Securitate Web & Headere", expanded=True):
        try:
            resp = requests.get(url, timeout=5)
            c1, c2 = st.columns(2)
            
            # HTTPS Check
            if url.startswith("https"):
                c1.success("✅ HTTPS este activat")
                raport_final += "[+] HTTPS: OK\n"
            else:
                c1.error("❌ HTTPS este INACTIV (Critic!)")
                raport_final += "[-] HTTPS: MISSING\n"
            
            # Server Info
            server = resp.headers.get("Server", "Unknown")
            c2.info(f"🖥️ Server detectat: {server}")
            raport_final += f"[*] Server: {server}\n"

            # Headers Check
            security_headers = ["X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security"]
            missing_count = 0
            for h in security_headers:
                if h in resp.headers:
                    st.write(f"✅ **{h}**: Prezent")
                    raport_final += f"[+] Header {h}: OK\n"
                else:
                    st.write(f"⚠️ **{h}**: Lipsește")
                    raport_final += f"[-] Header {h}: MISSING\n"
                    missing_count += 1
            
            if missing_count > 0:
                st.warning(f"S-au găsit {missing_count} probleme în configurarea headerelor.")

        except Exception as e:
            st.error(f"Eroare la conectare: {e}")
            raport_final += f"[!] Eroare critică: {e}\n"

    # 2. PORT SCANNER
    if scan_p:
        with st.expander("2. Porturi Deschise (Open Ports)", expanded=True):
            st.write(f"Scanez porturile pe {domain}...")
            # Eliminăm 'https://' pentru scanarea de porturi
            target_clean = domain.replace("https://", "").replace("http://", "").split("/")[0]
            
            try:
                open_ports = scan_ports(target_clean)
                cols = st.columns(3)
                idx = 0
                found_open = False
                
                for port, (service, status) in open_ports.items():
                    with cols[idx % 3]:
                        if "DESCHIS" in status:
                            st.error(f"🔴 {port} ({service}): {status}")
                            found_open = True
                            raport_final += f"[!] Port {port} ({service}): OPEN\n"
                        else:
                            st.success(f"🟢 {port} ({service}): {status}")
                    idx += 1
                
                if found_open:
                    st.warning("⚠️ Atenție! Există porturi deschise care pot fi vectori de atac.")
                else:
                    st.success("Toate porturile verificate par sigure.")
                    
            except Exception as e:
                st.error(f"Nu s-a putut scana porturile: {e}")

    # 3. SQL INJECTION
    if scan_sql:
        with st.expander("3. Test Vulnerabilitate SQL Injection", expanded=True):
            st.write("Verificăm parametrii URL pentru vulnerabilități de bază...")
            sql_results = check_sql_injection(url)
            
            for res in sql_results:
                if "Nu s-au detectat" in res:
                    st.success(f"✅ {res}")
                    raport_final += f"[+] SQLi: {res}\n"
                else:
                    st.warning(f"⚠️ {res}")
                    raport_final += f"[!] SQLi Check: {res}\n"

    # 4. EXPORT
    st.write("---")
    st.download_button("📥 Descarcă Raportul Complet (.txt)", raport_final, file_name="Raport_CyberScanner_v3.txt")