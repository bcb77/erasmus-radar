import os
import requests
from bs4 import BeautifulSoup
import json

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
HAFIZA_DOSYASI = "gecmis_ilanlar.txt"
VERITABANI = "projeler.json"

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": metin, "parse_mode": "HTML", "disable_web_page_preview": False}
    requests.post(url, data=payload)

def hafizayi_oku():
    if not os.path.exists(HAFIZA_DOSYASI): return []
    with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f: return f.read().splitlines()

def hafizaya_yaz(link):
    with open(HAFIZA_DOSYASI, "a", encoding="utf-8") as f: f.write(link + "\n")

def veritabanini_guncelle(yeni_ilanlar):
    """Bulunan projeleri Streamlit sitesinin okuması için JSON olarak kaydeder."""
    mevc_projeler = []
    if os.path.exists(VERITABANI):
        with open(VERITABANI, "r", encoding="utf-8") as f:
            try: mevc_projeler = json.load(f)
            except: pass
            
    guncel_liste = yeni_ilanlar + mevc_projeler
    with open(VERITABANI, "w", encoding="utf-8") as f:
        json.dump(guncel_liste[:30], f, ensure_ascii=False, indent=4)

def avci_bot():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    eski_linkler = hafizayi_oku()
    salto_ilanlar = []
    eplus_ilanlar = []
    
    # --- 1. HEDEF: SALTO (Fiziksel Filtreli ve Akıllı Link Kontrollü) ---
    try:
        res_salto = requests.get("https://www.salto-youth.net/tools/european-training-calendar/browse/", headers=headers)
        if res_salto.status_code == 200:
            soup = BeautifulSoup(res_salto.content, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/tools/european-training-calendar/training/" in href:
                    baslik = a.text.strip()
                    
                    # Akıllı Link Düzeltici: Eğer link zaten http ile başlıyorsa olduğu gibi bırak
                    if href.startswith("http"):
                        tam_link = href
                    else:
                        tam_link = "https://www.salto-youth.net" + (href if href.startswith("/") else "/" + href)
                    
                    if "online" in baslik.lower() or "virtual" in baslik.lower(): continue 
                    
                    if baslik and tam_link not in eski_linkler and tam_link not in [i["link"] for i in salto_ilanlar]:
                        salto_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "SALTO-YOUTH"})
    except Exception: pass

    # --- 2. HEDEF: E+ TÜRKİYE (Sıkı Filtreli ve Menü Ayıklayıcılı) ---
    try:
        res_eplus = requests.get("https://www.eplusturkiye.org/projeler/", headers=headers)
        if res_eplus.status_code == 200:
            soup_eplus = BeautifulSoup(res_eplus.content, "html.parser")
            for a in soup_eplus.find_all("a", href=True):
                href = a["href"]
                baslik = a.text.strip()
                
                # Sitenin menü sekmelerini ve çöpleri eleyen kara liste
                yasakli_kelimeler = [
                    "kvkk", "gizlilik", "iletişim", "hakkımızda", "anasayfa", "politika",
                    "work and travel", "geçmiş", "vizyon", "misyon", "sss", "sorular",
                    "hizmetlerimiz", "başvuru", "şartlar", "galeri", "blog", "dil okulu"
                ]
                gereksiz_mi = any(yasak in baslik.lower() for yasak in yasakli_kelimeler)
                
                # Başlık 30 karakterden uzun, içinde en az 2 tire (-) olan ve menü olmayan gerçek projeler
                if len(baslik) > 30 and not gereksiz_mi and href.count("-") >= 2 and href != "#" and not href.startswith("mailto:"):
                    tam_link = href if href.startswith("http") else "https://www.eplusturkiye.org" + (href if href.startswith("/") else "/" + href)
                    if tam_link not in eski_linkler and tam_link not in [i["link"] for i in eplus_ilanlar]:
                        eplus_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "Erasmus+ Türkiye"})
    except Exception: pass

    # --- GÖNDERİM VE VERİTABANI KAYDI ---
    gonderilecekler = salto_ilanlar[:3] + eplus_ilanlar[:3]
    
    if gonderilecekler:
        for ilan in gonderilecekler:
            mesaj = f"🚨 <b>YEPYENİ BİR PROJE YAYINLANDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> {ilan['platform']}\n\n🔗 <b>İncele:</b>\n{ilan['link']}"
            mesaj_gonder(mesaj)
            hafizaya_yaz(ilan['link'])
            
        # Hem Telegram'a atar hem de sitenin okuyacağı arşivi günceller
        veritabanini_guncelle(gonderilecekler)

if __name__ == "__main__":
    avci_bot()
