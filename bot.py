import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": metin, 
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

def avci_bot():
    url = "https://www.salto-youth.net/tools/european-training-calendar/browse/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers)
        
        # 1. Kontrol: Site bizi kapıdan çevirdi mi?
        if response.status_code != 200:
            mesaj_gonder(f"⚠️ <b>SALTO SİTESİ ERİŞİMİ REDDETTİ</b>\nDurum Kodu: {response.status_code}")
            return
            
        soup = BeautifulSoup(response.content, "html.parser")
        projeler = soup.find_all("div", class_="training-course") 
        
        # 2. Kontrol: Siteye girdik ama projelerin yerini bulamadık mı?
        if not projeler:
            site_basligi = soup.title.text if soup.title else "Başlık Bulunamadı"
            mesaj_gonder(f"✅ <b>BOT HEDEFE SIZDI AMA İLAN BULAMADI</b>\n\nSite Başlığı: <i>{site_basligi}</i>\n\nDurum: SALTO sayfasının tasarımı değişmiş olabilir, etiketleri bulamıyorum.")
            return

        # 3. Kontrol: İlanlar bulunduysa gönder!
        for proje in projeler[:3]: 
            baslik_etiketi = proje.find("h3")
            if not baslik_etiketi:
                continue
                
            baslik = baslik_etiketi.text.strip()
            link_etiketi = proje.find("a")
            link = "https://www.salto-youth.net" + link_etiketi["href"] if link_etiketi else url
            
            mesaj = f"🚨 <b>RADARA YENİ PROJE TAKILDI!</b>\n\n📌 <b>{baslik}</b>\n\n🌍 <b>Lokasyon:</b> Avrupa / Çevrimiçi\n\n🔗 <a href='{link}'>Detaylar İçin Tıkla</a>"
            mesaj_gonder(mesaj)
                
    except Exception as e:
        mesaj_gonder(f"❌ <b>SİSTEM HATASI:</b> {e}")

if __name__ == "__main__":
    avci_bot()
