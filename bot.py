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
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

def avci_bot():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    bulunan_ilanlar = []
    
    # HEDEF: SALTO-YOUTH
    try:
        salto_url = "https://www.salto-youth.net/tools/european-training-calendar/browse/"
        res_salto = requests.get(salto_url, headers=headers)
        
        if res_salto.status_code == 200:
            soup = BeautifulSoup(res_salto.content, "html.parser")
            
            for a in soup.find_all("a", href=True):
                href = a["href"]
                
                if "/tools/european-training-calendar/training/" in href:
                    baslik = a.text.strip()
                    
                    # --- ONLINE PROJE FİLTRESİ ---
                    baslik_kucuk = baslik.lower()
                    if "online" in baslik_kucuk or "virtual" in baslik_kucuk or "e-learning" in baslik_kucuk:
                        continue # Eğer bu kelimeler varsa, bu ilanı es geç ve sonrakine geç!
                        
                    if baslik and baslik not in [i["baslik"] for i in bulunan_ilanlar]:
                        bulunan_ilanlar.append({
                            "baslik": baslik, 
                            "link": "https://www.salto-youth.net" + href, 
                            "platform": "SALTO-YOUTH"
                        })
    except Exception as e:
        print(f"Tarama Hatası: {e}")

    # SONUÇLARI TELEGRAM'A GÖNDER
    if not bulunan_ilanlar:
        mesaj_gonder("⚠️ <b>SİTEYE GİRDİM AMA FİLTRELERİNE UYGUN FİZİKSEL BİR İLAN BULAMADIM.</b>")
        return
        
    for ilan in bulunan_ilanlar[:5]:
        mesaj = f"🚨 <b>YENİ FİZİKSEL PROJE TAKILDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> {ilan['platform']}\n\n🔗 <b>Başvuru Linki:</b>\n{ilan['link']}"
        mesaj_gonder(mesaj)

if __name__ == "__main__":
    avci_bot()
