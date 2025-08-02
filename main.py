import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# ✅ Telegram Config
BOT_TOKEN = '7807393497:AAES2bCHYdRtmx9PM6F35LjlyB8aVqrnKTA'
CHAT_ID = '-1002143117403'
bot = Bot(token=BOT_TOKEN)

# ✅ Cookie (latest you gave)
cookies = {
    "PHPSESSID": "eyJpdiI6ImU5eTdpYnpndDJIMzQ0N3VLVXA4Tmc9PSIsInZhbHVlIjoiTXpWRWFQU2Fpb0R3c2VLU1BqVDRkQVdvYVlOZ1RBdlhxYWJMSHZmM1dFMk0vdE95VEJMQUpGcElhZG1uUThabjVJVHJGRzAvK2lBNURFMXgzQms3SXcwRFpmZ1A3VFkxbGc2bzhrekJBeXR3NWVucjdtUW1vYk9Kem9YMG5rYU4iLCJtYWMiOiI4NzM2MDU3NDZmYzZlMGIxNjhmMTA2Y2M3OTJhMGUzNDQ4ZGU5Yzc2NjdiMDVlYWRjYzljMDRlNjVkN2ZmNDBiIiwidGFnIjoiIn0%3D"
}

def detect_service(message):
    if "facebook" in message.lower() or "fb-" in message.lower(): return "FACEBOOK"
    if "whatsapp" in message.lower(): return "WHATSAPP"
    if "telegram" in message.lower(): return "TELEGRAM"
    return "UNKNOWN"

def detect_country(number):
    number = number.replace("+", "")
    if number.startswith("225"): return "Côte d'Ivoire"
    elif number.startswith("51"): return "Peru"
    elif number.startswith("63"): return "Philippines"
    elif number.startswith("93"): return "Afghanistan"
    elif number.startswith("229"): return "Benin"
    elif number.startswith("84"): return "Vietnam"
    elif number.startswith("673"): return "Brunei"
    elif number.startswith("234"): return "Nigeria"
    elif number.startswith("44"): return "United Kingdom"
    elif number.startswith("1"): return "USA/Canada"
    elif number.startswith("880"): return "Bangladesh"
    elif number.startswith("91"): return "India"
    elif number.startswith("7"): return "Russia"
    elif number.startswith("62"): return "Indonesia"
    elif number.startswith("33"): return "France"
    elif number.startswith("20"): return "Egypt"
    elif number.startswith("974"): return "Qatar"
    elif number.startswith("90"): return "Turkey"
    elif number.startswith("30"): return "Greece"
    else: return "Unknown"

def scrape_otp():
    url = "https://www.ivasms.com/portal/live/my_sms"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table tr")

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            number = cols[1].text.strip()
            message = cols[4].text.strip()

            if not message:
                continue

            otp = ''.join(filter(str.isdigit, message))[:6]
            service = detect_service(message)
            country = detect_country(number)

            formatted = f"""🔔 {country} {service} OTP Received...

⚙️ Service: {service}
🌐 Country: {country}
☎️ Number: {number}
🔑 Your OTP: {otp}

✉️ Full-Message:
{message}

👨‍💻 Developer: @asik_2_0_bd
"""
            bot.send_message(chat_id=CHAT_ID, text=formatted)
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

# ✅ Run every 10 seconds
while True:
    scrape_otp()
    time.sleep(10)
