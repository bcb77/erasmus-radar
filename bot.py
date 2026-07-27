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
        if response.status_code != 200:
            return
            
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Sitedeki TÜM linkleri topluyoruz
        tum_linkler = soup.find_all("a", href=True)
        bulunan_ilanlar = []
        
        # Linklerin içinden sadece "eğitim ilanı" olanları cımbızlıyoruz
        for a_etiketi in tum_linkler:
            href = a_etiketi["href"]
            
            if "/tools/european-training-calendar/training/" in href:
                baslik = a_etiketi.text.strip()
                
                # Eğer başlık boş değilse ve listeye henüz eklemediysek
                if baslik and baslik not in [ilan["baslik"] for ilan in bulunan_ilanlar]:
                    tam_link = "https://www.salto-youth.net" + href
                    bulunan_ilanlar.append({"baslik": baslik, "link": tam_link})
        
        if not bulunan_ilanlar:
            mesaj_gonder("⚠️ <b>SİTEYE GİRDİM AMA İLAN LİNKLERİNİ AYIKLAYAMADIM.</b>")
            return
            
        # O 109 ilanın en güncel olan ilk 3 tanesini Telegram'a gönderiyoruz!
        for ilan in bulunan_ilanlar[:3]:
            mesaj = f"🚨 <b>RADARA YENİ PROJE TAKILDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> SALTO-YOUTH\n\n🔗 <a href='{ilan['link']}'>Detaylar ve Başvuru İçin Tıkla</a>"
            mesaj_gonder(mesaj)
            
    except Exception as e:
        mesaj_gonder(f"❌ <b>SİSTEM HATASI:</b> {e}")

if __name__ == "__main__":
    avci_bot()
