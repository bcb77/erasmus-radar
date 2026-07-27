import streamlit as st
import json
import os

# Sayfa ayarları (Koyu tema için hazır yapı)
st.set_page_config(page_title="Erasmus Radar", page_icon="🌍", layout="centered")

# Özel CSS ile arka planı siber/koyu tema konseptine çeviriyoruz
st.markdown(
    """
    <style>
    /* Ana arkaplanı şık bir koyu gri/lacivert tona boyuyoruz */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    /* Proje kartlarının arka planını hafif belirginleştiriyoruz */
    div.stContainer {
        background-color: #111827;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1f2937;
        margin-bottom: 15px;
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
