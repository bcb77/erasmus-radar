import os
import requests
from bs4 import BeautifulSoup
import json

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
HAFIZA_DOSYASI = "gecmis_ilanlar.txt"
VERITABANI = "projeler.json"

def mesaj_gonder(metin):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": metin, "parse_mode": "HTML", "disable_web_page_preview": False}
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")

def hafizayi_oku():
    if not os.path.exists(HAFIZA_DOSYASI): return []
    with open(HAFIZA_DOSYASI, "r", encoding="utf-8") as f: return f.read().splitlines()

def hafizaya_yaz(link):
    with open(HAFIZA_DOSYASI, "a", encoding="utf-8") as f: f.write(link + "\n")

def veritabanini_guncelle(yeni_ilanlar):
    mevc_projeler = []
    if os.path.exists(VERITABANI):
        with open(VERITABANI, "r", encoding="utf-8") as f:
            try: mevc_projeler = json.load(f)
            except: pass
            
    guncel_liste = yeni_ilanlar + mevc_projeler
    
    # Sitede çift/aynı projelerin görünmesini engelleyen benzersizleştirme filtresi
    benzersiz_liste = []
    gorulen_linkler = set()
    for p in guncel_liste:
        if p["link"] not in gorulen_linkler:
            benzersiz_liste.append(p)
            gorulen_linkler.add(p["link"])

    with open(VERITABANI, "w", encoding="utf-8") as f:
        json.dump(benzersiz_liste[:30], f, ensure_ascii=False, indent=4)

def avci_bot():
    # Güvenlik duvarlarını ve Cloudflare'i aşmak için gerçek bir tarayıcı taklidi yapan gelişmiş maske
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    
    eski_linkler = hafizayi_oku()
    salto_ilanlar = []
    eplus_ilanlar = []
    erasmusgram_ilanlar = []
    
    # --- 1. HEDEF: SALTO ---
    try:
        res_salto = requests.get("https://www.salto-youth.net/tools/european-training-calendar/browse/", headers=headers, timeout=15)
        if res_salto.status_code == 200:
            soup = BeautifulSoup(res_salto.content, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "tools/european-training-calendar/training/" in href:
                    baslik = a.text.strip()
                    idx = href.find("tools/european-training-calendar/training/")
                    temiz_kisim = href[idx:]
                    tam_link = "https://www.salto-youth.net/" + temiz_kisim
                    
                    if "online" in baslik.lower() or "virtual" in baslik.lower(): continue 
                    
                    if baslik and tam_link not in eski_linkler and tam_link not in [i["link"] for i in salto_ilanlar]:
                        salto_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "SALTO-YOUTH"})
    except Exception as e: print(f"SALTO Hatası: {e}")

    # --- 2. HEDEF: E+ TÜRKİYE ---
    try:
        res_eplus = requests.get("https://www.eplusturkiye.org/projeler/", headers=headers, timeout=15)
        if res_eplus.status_code == 200:
            soup_eplus = BeautifulSoup(res_eplus.content, "html.parser")
            for a in soup_eplus.find_all("a", href=True):
                href = a["href"]
                baslik = a.text.strip()
                
                yasakli_kelimeler = [
                    "kvkk", "gizlilik", "iletişim", "hakkımızda", "anasayfa", "politika",
                    "work and travel", "geçmiş", "vizyon", "misyon", "sss", "sorular",
                    "hizmetlerimiz", "başvuru", "şartlar", "galeri", "blog", "dil okulu"
                ]
                gereksiz_mi = any(yasak in baslik.lower() for yasak in yasakli_kelimeler)
                
                if len(baslik) > 30 and not gereksiz_mi and href.count("-") >= 2 and href != "#" and not href.startswith("mailto:"):
                    tam_link = href if href.startswith("http") else "https://www.eplusturkiye.org" + (href if href.startswith("/") else "/" + href)
                    if tam_link not in eski_linkler and tam_link not in [i["link"] for i in eplus_ilanlar]:
                        eplus_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "Erasmus+ Türkiye"})
        else:
            print(f"E+ Türkiye engelledi! HTTP Kodu: {res_eplus.status_code}")
    except Exception as e: print(f"E+ Türkiye Hatası: {e}")

    # --- 3. HEDEF: ERASMUSGRAM ---
    try:
        res_eg = requests.get("https://www.erasmusgram.com/category/avrupa-birligi-projeleri/", headers=headers, timeout=15)
        if res_eg.status_code == 200:
            soup_eg = BeautifulSoup(res_eg.content, "html.parser")
            for a in soup_eg.find_all("a", href=True):
                href = a["href"]
                baslik = a.text.strip()
                
                if "/category/" in href or "/tag/" in href or "/author/" in href or "page/" in href:
                    continue
                    
                # Sidebar'dan (yan menü) sızan BURS, STAJ, YÜKSEK LİSANS gibi ilgisiz duyuruları kesen katı filtre
                yasakli_kelimeler_eg = [
                    "kvkk", "gizlilik", "iletişim", "hakkımızda", "anasayfa", "politika",
                    "hizmetlerimiz", "başvuru", "şartlar", "devamını oku", "read more",
                    "burs", "staj", "iş ilanı", "yüksek lisans", "doktora", "çekiliş", "sonuçları"
                ]
                gereksiz_mi_eg = any(yasak in baslik.lower() for yasak in yasakli_kelimeler_eg)
                
                if len(baslik) > 20 and not gereksiz_mi_eg and href != "#":
                    tam_link = href if href.startswith("http") else "https://www.erasmusgram.com" + (href if href.startswith("/") else "/" + href)
                    if tam_link not in eski_linkler and tam_link not in [i["link"] for i in erasmusgram_ilanlar]:
                        erasmusgram_ilanlar.append({"baslik": baslik, "link": tam_link, "platform": "Erasmusgram"})
    except Exception as e: print(f"Erasmusgram Hatası: {e}")


    # --- GÖNDERİM VE VERİTABANI KAYDI ---
    gonderilecekler = salto_ilanlar[:4] + eplus_ilanlar[:4] + erasmusgram_ilanlar[:4]
    
    if gonderilecekler:
        for ilan in gonderilecekler:
            mesaj = f"🚨 <b>YEPYENİ BİR PROJE YAYINLANDI!</b>\n\n📌 <b>{ilan['baslik']}</b>\n\n🌍 <b>Platform:</b> {ilan['platform']}\n\n🔗 <b>İncele:</b>\n{ilan['link']}"
            mesaj_gonder(mesaj)
            hafizaya_yaz(ilan['link'])
            
        veritabanini_guncelle(gonderilecekler)
    else:
        # Bildirim mesajı şu an kapalı, aktif etmek istersen alttaki '#' işaretlerini kaldırabilirsin.
        # bilgi_mesaji = "ℹ️ <b>Radar Raporu:</b>\n\nŞu an için yeni bir fiziksel proje bulunamadı. Taramaya devam ediyorum! 🛰️"
        # mesaj_gonder(bilgi_mesaji)
        pass

if __name__ == "__main__":
    avci_bot()
