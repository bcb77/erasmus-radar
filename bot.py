import os
import requests

# Şifreleri GitHub'ın kasasından güvenli bir şekilde alıyoruz
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def mesaj_gonder(metin):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": metin,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response

# Şimdilik botun çalışıp çalışmadığını test ediyoruz
# Bir sonraki adımda buraya Avrupa Gençlik Portalı'nı tarayan kodları ekleyeceğiz!
test_mesaji = "🚨 *Sistem Aktif!*\n\nMerhaba! Ben Erasmus Radar Botu. Web tarama sistemim başarıyla kuruldu. Yeni projeler Türkiye'den başvuruya açıldığında sana buradan haber vereceğim!"

mesaj_gonder(test_mesaji)
