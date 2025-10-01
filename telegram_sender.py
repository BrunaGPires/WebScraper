import requests
import urllib.parse
import time
from config import TELEGRAM_CONFIG

class TelegramSender:
    def __init__(self):
        self.token = TELEGRAM_CONFIG['tbot_token']
        self.id = TELEGRAM_CONFIG['tele_id']

    def send_telegram_msg(self, filtered_news):
        for i, post in enumerate(filtered_news, 1):
            message = f"{i}. {post['title'][:100]}...\n{post['link']}"
            encoded_message = urllib.parse.quote(message)
            url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.id}&text={encoded_message}"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"Message {i} sent successfully.")
                else:
                    print(f"Error sending message {i}. Status code: {response.status_code}")
                time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
        return