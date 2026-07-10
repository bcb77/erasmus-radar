import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Erasmus Radar", layout="wide", page_icon="🌍")

st.title("🌍 Erasmus ve ESC Proje Radarı")
st.write("Türkiye'den başvuruya açık güncel projeler listesi.")

# Veriler (Saf sözlük yapısı - Pandas'a gerek yok!)
data = [
    {"Proje Adı": "Yeşil Dönüşüm Elçileri", "Tür": "Kısa Dönem ESC", "Ülke": "İspanya", "Şehir": "Madrid", "Süre": "2 Ay"},
    {"Proje Adı": "Dijital Gençlik Atölyesi", "Tür": "Gençlik Değişimi", "Ülke": "Almanya", "Şehir": "Berlin", "Süre": "10 Gün"},
    {"Proje Adı": "İklim ve Gelecek", "Tür": "Gençlik Değişimi", "Ülke": "İtalya", "Şehir": "Roma", "Süre": "14 Gün"},
    {"Proje Adı": "Kültürlerarası Köprü", "Tür": "Kısa Dönem ESC", "Ülke": "Polonya", "Şehir": "Varşova", "Süre": "1 Ay"},
    {"Proje Adı": "Sürdürülebilir Adımlar", "Tür": "Uzun Dönem ESC", "Ülke": "İspanya", "Şehir": "Barselona", "Süre": "10 Ay"}
]

col1, col2 = st.columns(2)

with col1:
    secilen_tur = st.selectbox("Proje Türü Seçin", ["Tümü", "Kısa Dönem ESC", "Gençlik Değişimi", "Uzun Dönem ESC"])
with col2:
    # Ülkeleri manuel veriyoruz, çökmeye mahal yok
    ulkeler = ["Tümü", "İspanya", "Almanya", "İtalya", "Polonya"]
    secilen_ulke = st.selectbox("Hedef Ülke", ulkeler)

st.markdown("---")

if st.button("Projeleri Getir"):
    with st.spinner('Senin için ilanlar filtreleniyor...'):
        
        # Filtreleme Mantığı (Saf Python - Işık hızında çalışır)
        filtered_data = [
            row for row in data 
            if (secilen_tur == "Tümü" or row["Tür"] == secilen_tur) and 
               (secilen_ulke == "Tümü" or row["Ülke"] == secilen_ulke)
        ]

        # Sonuçları Gösterme
        if not filtered_data:
            st.warning("Bu kriterlere uygun proje bulunamadı. Başka bir filtre dene!")
        else:
            st.success(f"Tam sana göre {len(filtered_data)} proje bulundu!")
            st.dataframe(filtered_data, use_container_width=True)
