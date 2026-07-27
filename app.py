import streamlit as st
import json
import os

# Sayfa ayarları
st.set_page_config(page_title="Erasmus Radar", page_icon="🌍", layout="centered")

# Özel CSS: Dünya haritası arka planı, yarı saydam kutular ve belirgin proje başlıkları
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(11, 15, 25, 0.90), rgba(11, 15, 25, 0.90)), url("https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Proje kutularını şık ve yarı saydam yapıyoruz */
    div.stContainer {
        background-color: rgba(17, 24, 39, 0.85);
        padding: 22px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin-bottom: 18px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* Proje başlıklarını çok daha belirgin ve dikkat çekici yapıyoruz */
    div.stContainer h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Erasmus & ESC Proje Radarı")
st.markdown("Botumuzun internetteki platformlardan senin için otomatik olarak topladığı en güncel fiziksel projeler aşağıda listelenmiştir.")
st.divider()

VERITABANI = "projeler.json"

# Veritabanını okuyup ekrana yansıtma işlemi
if os.path.exists(VERITABANI):
    with open(VERITABANI, "r", encoding="utf-8") as f:
        try:
            projeler = json.load(f)
            
            if not projeler:
                st.info("Şu an için sistemde kayıtlı yeni bir proje bulunmuyor.")
            else:
                for proje in projeler:
                    with st.container():
                        st.subheader(f"📌 {proje['baslik']}")
                        st.caption(f"**Platform:** {proje['platform']}")
                        
                        # Tıklanabilir başvuru butonu
                        st.link_button("Hemen Başvur / İncele", proje['link'])
        except:
            st.error("Veriler okunurken bir hata oluştu. Veritabanı formatı bozuk olabilir.")
else:
    st.warning("Henüz hiç proje toplanmadı. Bot ilk taramasını yaptıktan sonra ilanlar burada görünecektir.")
