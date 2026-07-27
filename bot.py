import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
HAFIZA_DOSYASI = "gecmis_ilanlar.txt"

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": metin, 
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

def hafizayi_oku():
    """Botun daha önce gönderdiği linkleri hatırlar."""
    if not os.path.exists(HAFIZA_DOSYASI):
        return []
    with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def hafizaya_yaz(link):
    """Yeni gönderilen linki kara kaplı deftere yazar."""
    with open(HAFIZA_DOSYASI, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def avci_bot():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    eski_linkler = hafizayi_oku()
    yeni_ilanlar = []
    
    # --- 1. HEDEF: SALTO-YOUTH (Sadece Fiziksel) ---
    try:
        salto_url = "https://www.salto-youth.net/tools/european-training-calendar/browse/"
        res_salto = requests.get(salto_url, headers=headers)
        if res_salto.status_code == 200:
            soup = BeautifulSoup(res_salto.content, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/tools/european-training-calendar/training/" in href:
                    baslik = a.text.strip()
                    tam_link = "https://www.salto-youth.net" + href
                    
                    baslik_kucuk = baslik.lower()
                    if "online" in baslik_kucuk or "virtual" in baslik_kucuk or "e-learning" in baslik_kucuk:
                        continue 
                        
                    if baslik and tam_link not in eski_linkler:
                        if tam_link not in [i["link"] for i in yeni_ilanlar]:
                            yeni_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "SALTO-YOUTH"})
    except Exception as e:
        print(f"SALTO Hatası: {e}")

    # --- 2. HEDEF: ERASMUS+ TÜRKİYE (Tüm Projeler, Ayrım Yok) ---
    try:
        eplus_url = "https://www.eplusturkiye.org/projeler/"
        res_eplus = requests.get(eplus_url, headers=headers)
        if res_eplus.status_code == 200:
            soup_eplus = BeautifulSoup(res_eplus.content, "html.parser")
            
            for a in soup_eplus.find_all("a", href=True):
                href = a["href"]
                baslik = a.text.strip()
                
                # Sitedeki "Anasayfa", "Hakkımızda" gibi kısa menü linklerini eleyip sadece uzun başlıklı (15+ karakter) proje linklerini alıyoruz
                if len(baslik) > 15 and href != "#" and not href.startswith("mailto:"):
                    # Linkin başına site adresini ekleyip tam tıklanabilir hale getiriyoruz
                    tam_link = href if href.startswith("http") else "https://www.eplusturkiye.org" + (href if href.startswith("/") else "/" + href)
                    
                    # Hafızada yoksa direkt listeye ekliyoruz, online/fiziksel ayrımı yok!
                    if tam_link not in eski_linkler:
                        if tam_link not in [i["link"] for i in yeni_ilanlar]:
                            yeni_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "Erasmus+ Türkiye"})
    except Exception as e:
        print(f"E+ Türkiye Hatası: {e}")

    # --- YENİ İLANLARI TELEGRAM'A GÖNDER VE HAFIZAYA KAYDET ---
    if not yeni_ilanlar:
        print("Yeni ilan bulunamadı. Bot uykuya dönüyor.")
        return
        
    for ilan in yeni_ilanlar[:5]:
        mesaj = f"🚨 <b>YEPYENİ BİR PROJE YAYINLANDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> {ilan['platform']}\n\n🔗 <b>İncele:</b>\n{ilan['link']}"
        mesaj_gonder(mesaj)
        hafizaya_yaz(ilan['link']) 

if __name__ == "__main__":
    avci_bot()
