import streamlit as st
import requests

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Scanner Vulnerabilități", page_icon="🛡️")

st.title("🛡️ Web Vulnerability Scanner")
st.write("Verifică securitatea de bază a unui site web.")

# --- ZONA DE INPUT ---
url = st.text_input("Introdu URL-ul țintă (ex: https://google.com):", "")

# --- BUTONUL DE START ---
if st.button("Începe Scanarea"):
    if not url:
        st.warning("Te rog introdu un link valid!")
    else:
        try:
            with st.spinner(f"Mă conectez la {url}..."):
                # Facem cererea către site
                response = requests.get(url, timeout=5)
            
            # 1. Verificare HTTPS
            st.subheader("1. Conexiune Securizată")
            if url.startswith("https"):
                st.success("✅ Site-ul folosește HTTPS.")
            else:
                st.error("❌ Site-ul folosește HTTP (Nesecurizat!).")

            # 2. Verificare Headere
            st.subheader("2. Headere de Securitate")
            
            headers_lista = {
                "X-Frame-Options": "Previne atacurile Clickjacking.",
                "Content-Security-Policy": "Protecție contra XSS.",
                "Strict-Transport-Security": "Forțează conexiunea criptată."
            }

            for header, descriere in headers_lista.items():
                if header in response.headers:
                    st.success(f"✅ {header} este activ.")
                else:
                    st.warning(f"⚠️ {header} LIPSEȘTE.")
                    st.caption(f"ℹ️ {descriere}")

        except Exception as e:
            st.error(f"Nu s-a putut accesa site-ul. Eroare: {e}")