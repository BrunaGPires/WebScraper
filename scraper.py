import requests
import smtplib, ssl
import os
import time
import urllib.parse
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

email_config = {
    "sender_mail" : os.getenv('SENDER_EMAIL'),
    "receiver_mail" : os.getenv('RECEIVER_EMAIL'),
    "password": os.getenv('EMAIL_PASSWORD')
}

telegram_token = {
    "tbot_token" : os.getenv('TELEGRAM_TOKEN'),
    "tele_id" : os.getenv('TELE_ID')
}

key_words = [
    "London", "Europe", "EUIC", "UK", "United Kingdom", "England", "Lisbon", "Natural History Museum", "Excel Center", "Excel Centre"
]

# Site Scraper
def scraper_serebii():
    serebii_url = "https://serebii.net/"

    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
    }
    
    all_news = []

    try:
        print("Fazendo requisição...")

        response = requests.get(serebii_url, headers=HEADERS)
        response.raise_for_status()

        print(f"Status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Procura todos elementos com classe 'post'
        post_elements = soup.find_all(lambda tag: tag.has_attr('class') and 'post' in tag['class'])

        for i, post in enumerate(post_elements):
            # Inicializa variveis
            title = ""
            full_link = ""
            post_paragraph = []

            # Pega o h2 e p que estão em post
            h2s = post.find_all('h2', recursive=True)
            ps = post.find_all('p', recursive=True)
            for h2 in h2s:
                title_text = h2.get_text(strip=True)
                title = title_text
                # Pegar o link do post
                a = h2.find("a")
                if a and a.has_attr("href"):
                    link = a["href"]
                    full_link = f"https://www.serebii.net{link}"
            for p in ps:
                p_text = p.get_text(strip=True)
                post_paragraph.append(p_text)

            news_data = {
                "id" : i + 1,
                "title" : title,
                "post_paragraph" : post_paragraph,
                "link" : full_link
            }

            all_news.append(news_data)

        return all_news
    
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Filter based on key words
def filter(all_news, key_words):
    filtered_posts = []

    for posts in all_news:
        text = ' '.join(posts['post_paragraph']).lower()
        title = posts['title'].lower()

        for word in key_words:
            word_lower = word.lower()
            if word_lower in title or word_lower in text:
                filtered_posts.append(posts)
                break

    return filtered_posts

# Send emails
def mail_sender(all_news, filtered_news):
    #Config
    sender_mail = email_config['sender_mail']
    receiver_mail = email_config["receiver_mail"]
    password = email_config["password"]

    port = 587  
    context = ssl.create_default_context()

    body_text = []
    for post in filtered_news:
        body_text.append(f"Title: {post['title']}")
        body_text.append(f"Link: {post['link']}")
        body_text.append("")

    # Email content
    subject = "Pokemon London / Europe Notifier"
    body = "\n".join(body_text)

    msg = MIMEMultipart()
    msg["From"] = sender_mail
    msg["To"] = receiver_mail
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        print("Connecting to SMTP server...")
        with smtplib.SMTP("smtp.gmail.com", port) as server:
            server.ehlo()
            server.starttls(context=context)
            print("Logging in...")
            server.login(sender_mail, password)
            print("Sending email...")
            server.sendmail(sender_mail, receiver_mail, msg.as_string())
            server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Erro: {e}")
        return None

    return

# Send Telegram Message
def telegram_sender(filtered_news):
    # config
    token = telegram_token["tbot_token"]
    id = telegram_token["tele_id"]

    for i, post in enumerate(filtered_news, 1):
        message = f"{i}. {post['title'][:100]}...\n{post['link']}"
        encoded_message = urllib.parse.quote(message)
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={encoded_message}"
        
        try:
            response = requests.get(url)
            print("Status Code:", response.status_code)
            time.sleep(1)
        except Exception as e:
            print(f"Erro: {e}")
    return

if __name__ == "__main__":
    all_news = scraper_serebii()

    if all_news:        
        filtered_news = filter(all_news, key_words)

        print(f"Total de posts encontrados: {len(all_news)}")
        print(f"Posts filtrados: {len(filtered_news)}")

        for post in filtered_news:
            print(f"\n→ {post['title']}")
            print(f"  Link: {post['link']}")
        if filtered_news:
            mail_sender(all_news, filtered_news)
            telegram_sender(filtered_news)
    else:
        print("\nFalha ao obter HTML.")