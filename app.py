import streamlit as st

# Sitenin sekme adı ve genişliği
st.set_page_config(page_title="Erasmus Radar", layout="wide")

# Ana Başlık
st.title("🌍 Erasmus ve ESC Proje Radarı")
st.write("Türkiye'den başvuruya açık projeleri yakında burada göreceksin!")

# Görsel bir filtre (Şimdilik test amaçlı)
proje_turu = st.selectbox("Proje Türü Seçin", ["Tümü", "Kısa Dönem ESC", "Gençlik Değişimi"])

if st.button("Projeleri Getir"):
    st.success(f"{proje_turu} için ilanlar aranıyor... (Veri çekme botu eklenecek!)")
