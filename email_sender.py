import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_CONFIG

class EmailSender:
    def __init__(self):
        self.email_from = EMAIL_CONFIG['sender_mail']
        self.email_to = EMAIL_CONFIG['receiver_mail']
        self.email_password = EMAIL_CONFIG['password']
        self.smtp_server = EMAIL_CONFIG.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = EMAIL_CONFIG.get('smtp_port', 587)

    def create_email_body(self, filtered_news):
        body_text = []
        for post in filtered_news:
            body_text.append(f"Title: {post['title']}")
            body_text.append(f"Link: {post['link']}")
            body_text.append("")
        return "\n".join(body_text)

    def send_email(self, filtered_news):
        context = ssl.create_default_context()

        subject = "Pokemon London / Europe Notifier"
        body = self.create_email_body(filtered_news)

        msg = MIMEMultipart()
        msg["From"] = self.email_from
        msg["To"] = self.email_to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            print("Connecting to SMTP server...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                print("Logging in...")
                server.login(self.email_from, self.email_password)
                print("Sending email...")
                server.sendmail(self.email_from, self.email_to, msg.as_string())
                server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Erro: {e}")
            return None

        return