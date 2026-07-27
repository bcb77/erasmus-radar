import streamlit as st
import json
import os

# Sayfa ayarları
st.set_page_config(page_title="Erasmus Radar", page_icon="🌍", layout="centered")

# CSS: Butonları canlı maviye boyayan, yazıları netleştiren tasarım
st.markdown(
    """
    <style>
    /* Arka plan görseli ve karartması */
    .stApp {
        background-image: linear-gradient(rgba(5, 8, 15, 0.93), rgba(5, 8, 15, 0.93)), url("https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Ana başlık ve metinlerin rengini tamamen beyaz yapıyoruz */
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
    }

    /* Proje kutularını daha belirgin ve şık bir cam efektine dönüştürüyoruz */
    div.stContainer {
        background-color: rgba(17, 24, 39, 0.90);
        padding: 22px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    /* Proje başlıkları (parlak mavi tonuyla dikkat çekici) */
    div.stContainer h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    
    /* Platform ve küçük yazılar */
    div.stContainer p {
        color: #e2e8f0 !important;
    }

    /* Hemen Başvur butonunu canlı mavi renk ve net beyaz yazıyla belirginleştiriyoruz */
    div.stContainer a {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
    }
    div.stContainer a:hover {
        background-color: #1d4ed8 !important;
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
