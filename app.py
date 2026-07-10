import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Erasmus Radar", layout="wide", page_icon="🌍")

st.title("🌍 Erasmus ve ESC Proje Radarı")
st.write("Türkiye'den başvuruya açık güncel projeler listesi.")

# Botun çekeceği verilerin şimdilik simülasyonu
data = {
    "Proje Adı": ["Yeşil Dönüşüm Elçileri", "Dijital Gençlik Atölyesi", "İklim ve Gelecek", "Kültürlerarası Köprü", "Sürdürülebilir Adımlar"],
    "Tür": ["Kısa Dönem ESC", "Gençlik Değişimi", "Gençlik Değişimi", "Kısa Dönem ESC", "Uzun Dönem ESC"],
    "Ülke": ["İspanya", "Almanya", "İtalya", "Polonya", "İspanya"],
    "Şehir": ["Madrid", "Berlin", "Roma", "Varşova", "Barselona"],
    "Süre": ["2 Ay", "10 Gün", "14 Gün", "1 Ay", "10 Ay"]
}
df = pd.DataFrame(data)

# Filtreleri yan yana koymak için sütunlar oluşturuyoruz
col1, col2 = st.columns(2)

with col1:
    secilen_tur = st.selectbox("Proje Türü Seçin", ["Tümü", "Kısa Dönem ESC", "Gençlik Değişimi", "Uzun Dönem ESC"])
with col2:
    # Ülkeleri veri setinden otomatik çekip listeliyoruz
    ulkeler = ["Tümü"] + list(df["Ülke"].unique())
    secilen_ulke = st.selectbox("Hedef Ülke", ulkeler)

st.markdown("---")

if st.button("Projeleri Getir"):
    with st.spinner('Senin için ilanlar filtreleniyor...'):
        
        # Filtreleme Mantığı
        filtered_df = df.copy()
        if secilen_tur != "Tümü":
            filtered_df = filtered_df[filtered_df["Tür"] == secilen_tur]
        if secilen_ulke != "Tümü":
            filtered_df = filtered_df[filtered_df["Ülke"] == secilen_ulke]

        # Sonuçları Gösterme
        if filtered_df.empty:
            st.warning("Bu kriterlere uygun proje bulunamadı. Başka bir filtre dene!")
        else:
            st.success(f"Tam sana göre {len(filtered_df)} proje bulundu!")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
