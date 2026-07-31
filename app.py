import streamlit as st
import json
import os

# Sayfa ayarları
st.set_page_config(page_title="Erasmus Radar", page_icon="🌍", layout="centered")

# CSS: Renkli siyasi harita arka planı, 0.69 karartma, cam efektli kutular ve beyaz yazılar
st.markdown(
    """
    <style>
    .stApp {
        /* 0.69 Karartma ve Kendi GitHub Linkin */
        background-image: linear-gradient(rgba(5, 8, 15, 0.69), rgba(5, 8, 15, 0.69)), url("https://raw.githubusercontent.com/bcb77/erasmus-radar/main/Harita%20g%C3%B6rseli.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
    }

    div.stContainer {
        background-color: rgba(17, 24, 39, 0.88);
        padding: 22px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    div.stContainer h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    
    div.stContainer p {
        color: #e2e8f0 !important;
    }

    .stLinkButton a {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
    }
    .stLinkButton a:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }
    .stLinkButton a p {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Erasmus & ESC Proje Radarı")
st.markdown("Botumuzun internetteki platformlardan senin için otomatik olarak topladığı en güncel fiziksel projeler aşağıda listelenmiştir.")
st.divider()

VERITABANI = "projeler.json"

# Güvenli Veri Okuma Mekanizması
projeler = []
if os.path.exists(VERITABANI):
    try:
        with open(VERITABANI, "r", encoding="utf-8") as f:
            icerik = f.read()
            if icerik.strip():
                projeler = json.loads(icerik)
    except:
        projeler = []

# Ekrana yansıtma
if not projeler:
    st.info("🛰️ **Radar Aktif!** Bot arka planda tarama yapıyor. Yeni projeler düştüğünde anında burada listelenecektir.")
else:
    for proje in projeler:
        with st.container():
            baslik = proje.get("baslik", "İsimsiz Proje")
            platform = proje.get("platform", "Erasmus+")
            link = proje.get("link", "#")
            
            # --- GEÇMİŞTEN KALAN BOZUK LİNKLERİ TEMİZLEME FİLTRESİ ---
            if "salto-youth.net" in link and "tools/european-training-calendar/training/" in link:
                idx = link.find("tools/european-training-calendar/training/")
                link = "https://www.salto-youth.net/" + link[idx:]
            # -----------------------------------------------------------
            
            st.subheader(f"📌 {baslik}")
            st.caption(f"**Platform:** {platform}")
            st.link_button("Hemen Başvur / İncele", link)
