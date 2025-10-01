from dotenv import load_dotenv
from scraper import SerebiiScraper
from filter import Filter
from email_sender import EmailSender
from telegram_sender import TelegramSender

load_dotenv()

def main():
    scraper = SerebiiScraper()
    news_filter = Filter()
    email_sender = EmailSender()
    telegram_sender = TelegramSender()

    all_news = scraper.scrape_serebii()

    if all_news:        
        filtered_news = news_filter.filter_news(all_news)

        print(f"Total de posts encontrados: {len(all_news)}")
        print(f"Posts filtrados: {len(filtered_news)}")

        for post in filtered_news:
            print(f"\n→ {post['title']}")
            print(f"  Link: {post['link']}")
        
        if filtered_news:
            email_sender.send_email(filtered_news)
            telegram_sender.send_telegram_msg(filtered_news)
        else:
            print("Nenhuma notícia relevante encontrada.")
    else:
        print("\nFalha ao obter HTML.")

if __name__ == "__main__":
    main()