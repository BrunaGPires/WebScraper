import os
from dotenv import load_dotenv

load_dotenv()

PROXY_CONFIG = {
    'http' : os.getenv('HTTP'),
    'https' : os.getenv('HTTPS')
}

# email
EMAIL_CONFIG = {
    "sender_mail" : os.getenv('SENDER_EMAIL'),
    "receiver_mail" : os.getenv('RECEIVER_EMAIL'),
    "password": os.getenv('EMAIL_PASSWORD'),
    "smtp_server": "smtp.gmail.com",
    "smtp_port" : 587
}

# telegram
TELEGRAM_CONFIG = {
    "tbot_token" : os.getenv('TELEGRAM_TOKEN'),
    "tele_id" : os.getenv('TELE_ID')
}

# key words
KEY_WORDS = [
    "London", "Europe", "EUIC", "UK", "United Kingdom", "England", "Lisbon", "Natural History Museum", "Excel Center", "Excel Centre"
]