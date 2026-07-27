import os
import requests
from bs4 import BeautifulSoup

# Kasadan şifrelerimizi alıyoruz
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def mesaj_gonder(metin):
    """Telegram'a HTML formatında şık bir mesaj atar."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": metin, 
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

def avci_bot():
    """Hedef siteyi tarayan ve verileri kazıyan ana komuta merkezi."""
    
    # Şimdilik SALTO-YOUTH'un eğitim takvimini hedef alıyoruz. 
    url = "https://www.salto-youth.net/tools/european-training-calendar/browse/"
    
    # Bot olduğumuzu belli etmemek için kendimizi standart bir tarayıcı gibi gösteriyoruz
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Sitedeki proje listelerinin olduğu HTML etiketlerini buluyoruz
        projeler = soup.find_all("div", class_="training-course") 
        
        yeni_ilan_bulundu_mu = False
        
        # En üstteki (en yeni) 3 ilana bakalım
        for proje in projeler[:3]: 
            baslik_etiketi = proje.find("h3")
            if not baslik_etiketi:
                continue
                
            baslik = baslik_etiketi.text.strip()
            link_etiketi = proje.find("a")
            # Sitenin ana URL'si ile ilanın uzantısını birleştiriyoruz
            link = "https://www.salto-youth.net" + link_etiketi["href"] if link_etiketi else url
            
            # Eğer bu projeyi daha önce sana göndermediysem:
            if not hafizada_var_mi(baslik):
                mesaj = f"🚨 <b>RADARA YENİ PROJE TAKILDI!</b>\n\n📌 <b>{baslik}</b>\n\n🌍 <b>Lokasyon:</b> Avrupa / Çevrimiçi (Linkten kontrol et)\n\n🔗 <a href='{link}'>Detaylar ve Başvuru İçin Tıkla</a>"
                mesaj_gonder(mesaj)
                hafizaya_yaz(baslik)
                yeni_ilan_bulundu_mu = True
                
        if not yeni_ilan_bulundu_mu:
            print("Sistem taramayı tamamladı, şu an için yeni proje yok.")
                
    except Exception as e:
        print(f"Hedef siteye sızarken bir sorun oluştu: {e}")

def hafizada_var_mi(baslik):
    """Bu projeyi daha önce telegram'dan gönderdik mi diye kontrol eder."""
    if not os.path.exists("gecmis_ilanlar.txt"):
        return False
    with open("gecmis_ilanlar.txt", "r", encoding="utf-8") as f:
        return baslik in f.read()

def hafizaya_yaz(baslik):
    """Gönderilen projeyi bir daha göndermemek için kara kaplı deftere yazar."""
    with open("gecmis_ilanlar.txt", "a", encoding="utf-8") as f:
        f.write(baslik + "\n")

if __name__ == "__main__":
    avci_bot()
