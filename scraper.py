import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from config import PROXY_CONFIG

load_dotenv()

class SerebiiScraper:
    def __init__(self):
        self.serebii_url = "https://serebii.net/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "accept": "*/*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
        }

    def scrape_serebii(self):        
        all_news = []

        try:
            print("Fazendo requisição...")

            response = requests.get(self.serebii_url, headers=self.headers, proxies=PROXY_CONFIG)
            response.raise_for_status()

            print(f"Status: {response.status_code}")
            soup = BeautifulSoup(response.text, "html.parser")

            # Search for all elements with class 'post'
            post_elements = soup.find_all(lambda tag: tag.has_attr('class') and 'post' in tag['class'])

            for i, post in enumerate(post_elements):
                # Initialize variables
                title = ""
                full_link = ""
                post_paragraph = []

                # Get the h2 and p inside post
                h2s = post.find_all('h2', recursive=True)
                ps = post.find_all('p', recursive=True)

                for h2 in h2s:
                    title_text = h2.get_text(strip=True)
                    title = title_text
                    # Get the post link
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
            print(f"Erro in scraping: {e}")
            return None