import streamlit as st
import json
import os

# Sayfa ayarları
st.set_page_config(page_title="Erasmus Radar", page_icon="🌍", layout="centered")

# CSS: Arka plan, cam efektli kutular ve genel metin ayarları
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

    /* Proje kutularını cam efektli yapıyoruz */
    div.stContainer {
        background-color: rgba(17, 24, 39, 0.90);
        padding: 22px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.4);
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    }

    /* Proje başlıkları (parlak mavi tonu) */
    div.stContainer h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    
    /* Platform ve küçük yazılar */
    div.stContainer p {
        color: #e2e8f0 !important;
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
                st.info("Şu an için sistemde kayıtlı yeni bir proje bulun\nuyor.")
            else:
                for proje in projeler:
                    with st.container():
                        st.subheader(f"📌 {proje['baslik']}")
                        st.caption(f"**Platform:** {proje['platform']}")
                        
                        # %100 garantili, canlı mavi renkli ve beyaz yazılı özel HTML buton
                        st.markdown(
                            f'''
                            <div style="margin-top: 12px;">
                                <a href="{proje['link']}" target="_blank" style="
                                    background-color: #2563eb; 
                                    color: #ffffff !important; 
                                    padding: 10px 20px; 
                                    border-radius: 8px; 
                                    font-weight: 600; 
                                    text-decoration: none; 
                                    display: inline-block;
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                                ">🚀 Hemen Başvur / İncele</a>
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
        except:
            st.error("Veriler okunurken bir hata oluştu. Veritabanı formatı bozuk olabilir.")
else:
    st.warning("Henüz hiç proje toplanmadı. Bot ilk taramasını yaptıktan sonra ilanlar burada görünecektir.")
