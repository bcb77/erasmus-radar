import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
HAFIZA_DOSYASI = "gecmis_ilanlar.txt"

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": metin, "parse_mode": "HTML", "disable_web_page_preview": False}
    requests.post(url, data=payload)

def hafizayi_oku():
    if not os.path.exists(HAFIZA_DOSYASI): return []
    with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f: return f.read().splitlines()

def hafizaya_yaz(link):
    with open(HAFIZA_DOSYASI, "a", encoding="utf-8") as f: f.write(link + "\n")

def avci_bot():
    # --- YENİ KİMLİK KARTI ---
    # Artık siteye sadece "Ben Chrome'um" demiyoruz, ne istediğimizi ve dilimizi de söylüyoruz.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    eski_linkler = hafizayi_oku()
    salto_ilanlar = []
    eplus_ilanlar = []
    e_plus_durum_mesaji = ""
    
    # --- 1. HEDEF: SALTO ---
    try:
        res_salto = requests.get("https://www.salto-youth.net/tools/european-training-calendar/browse/", headers=headers)
        if res_salto.status_code == 200:
            soup = BeautifulSoup(res_salto.content, "html.parser")
            for a in soup.find_all("a", href=True):
                if "/tools/european-training-calendar/training/" in a["href"]:
                    baslik = a.text.strip()
                    tam_link = "https://www.salto-youth.net" + a["href"]
                    if "online" in baslik.lower() or "virtual" in baslik.lower(): continue 
                    
                    if baslik and tam_link not in eski_linkler and tam_link not in [i["link"] for i in salto_ilanlar]:
                        salto_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "SALTO-YOUTH"})
    except Exception: pass

    # --- 2. HEDEF: E+ TÜRKİYE ---
    try:
        res_eplus = requests.get("https://www.eplusturkiye.org/projeler/", headers=headers)
        if res_eplus.status_code != 200:
            e_plus_durum_mesaji = f"Site erişimi reddetti. (Durum Kodu: {res_eplus.status_code})"
        else:
            soup_eplus = BeautifulSoup(res_eplus.content, "html.parser")
            
            for a in soup_eplus.find_all("a", href=True):
                href = a["href"]
                baslik = a.text.strip()
                
                yasakli_kelimeler = ["kvkk", "gizlilik", "iletişim", "hakkımızda", "anasayfa", "politika"]
                gereksiz_mi = any(yasak in baslik.lower() for yasak in yasakli_kelimeler)
                
                if len(baslik) > 15 and not gereksiz_mi and href != "#" and not href.startswith("mailto:"):
                    tam_link = href if href.startswith("http") else "https://www.eplusturkiye.org" + (href if href.startswith("/") else "/" + href)
                    if tam_link not in eski_linkler and tam_link not in [i["link"] for i in eplus_ilanlar]:
                        eplus_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "Erasmus+ Türkiye"})
                        
            if not eplus_ilanlar:
                e_plus_durum_mesaji = "Siteye başarıyla sızıldı (Kod 200) ama şu an aktif bir proje linki yok."
    except Exception as e:
        e_plus_durum_mesaji = f"Tarama Hatası: {e}"

    # --- GÖNDERİM VE HAFIZA KAYDI ---
    gonderilecekler = salto_ilanlar[:3] + eplus_ilanlar[:3]
    
    for ilan in gonderilecekler:
        mesaj = f"🚨 <b>YEPYENİ BİR PROJE YAYINLANDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> {ilan['platform']}\n\n🔗 <b>İncele:</b>\n{ilan['link']}"
        mesaj_gonder(mesaj)
        hafizaya_yaz(ilan['link'])
        
    if e_plus_durum_mesaji and not eplus_ilanlar:
        mesaj_gonder(f"⚠️ <b>E+ TÜRKİYE TEŞHİS RAPORU:</b>\n{e_plus_durum_mesaji}")

if __name__ == "__main__":
    avci_bot()
