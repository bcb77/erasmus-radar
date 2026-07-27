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
        "disable_web_page_preview": False  # Link önizlemesini açtık
    }
    requests.post(url, data=payload)

def avci_bot():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    bulunan_ilanlar = []
    
    # --- 1. HEDEF: SALTO-YOUTH ---
    try:
        salto_url = "https://www.salto-youth.net/tools/european-training-calendar/browse/"
        res_salto = requests.get(salto_url, headers=headers)
        if res_salto.status_code == 200:
            soup = BeautifulSoup(res_salto.content, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/tools/european-training-calendar/training/" in href:
                    baslik = a.text.strip()
                    if baslik and baslik not in [i["baslik"] for i in bulunan_ilanlar]:
                        bulunan_ilanlar.append({
                            "baslik": baslik, 
                            "link": "https://www.salto-youth.net" + href, 
                            "platform": "SALTO-YOUTH"
                        })
    except Exception as e:
        print(f"SALTO Tarama Hatası: {e}")

    # --- 2. HEDEF: AVRUPA GENÇLİK PORTALI (ESC / Erasmus+) ---
    try:
        esc_url = "https://youth.europa.eu/solidarity/projects_en"
        res_esc = requests.get(esc_url, headers=headers)
        if res_esc.status_code == 200:
            soup_esc = BeautifulSoup(res_esc.content, "html.parser")
            for a in soup_esc.find_all("a", href=True):
                href = a["href"]
                # ESC sitesindeki proje linklerini cımbızlıyoruz
                if "/solidarity/placement/" in href or "/solidarity/project/" in href:
                    baslik = a.text.strip() or "Avrupa Gençlik Portalı İlanı"
                    if baslik and baslik not in [i["baslik"] for i in bulunan_ilanlar]:
                        tam_link = href if href.startswith("http") else "https://youth.europa.eu" + href
                        bulunan_ilanlar.append({
                            "baslik": baslik, 
                            "link": tam_link, 
                            "platform": "Avrupa Gençlik Portalı"
                        })
    except Exception as e:
        print(f"ESC Tarama Hatası: {e}")

    # --- SONUÇLARI TELEGRAM'A GÖNDER ---
    if not bulunan_ilanlar:
        mesaj_gonder("⚠️ <b>SİTELERE GİRDİM AMA YENİ İLAN BULAMADIM.</b>")
        return
        
    # İlan limitini 3'ten 5'e çıkardık!
    for ilan in bulunan_ilanlar[:5]:
        # Linki tıklanabilir olması için açık açık alta yazıyoruz
        mesaj = f"🚨 <b>YENİ PROJE TAKILDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> {ilan['platform']}\n\n🔗 <b>Başvuru Linki:</b>\n{ilan['link']}"
        mesaj_gonder(mesaj)

if __name__ == "__main__":
    avci_bot()
