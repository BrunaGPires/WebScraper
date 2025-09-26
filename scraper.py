import requests
from bs4 import BeautifulSoup
import re
import json

key_words = [
    "London", "Europe", "EUIC", "UK", "United Kingdom", "England", "Lisbon", "Natural History Museum", "Excel Center", "Excel Centre"
]

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

        response = requests.get(serebii_url, headers=HEADERS, proxies=proxy_config)
        response.raise_for_status()

        print(f"Status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # Procura todos elementos com classe 'post'
        post_elements = soup.find_all(lambda tag: tag.has_attr('class') and 'post' in tag['class'])

        # Inicializa variveis para o json
        title = ""
        full_link = ""
        post_paragraph = []

        for i, post in enumerate(post_elements):
            print(f"\n{'='*60}")
            print(f"POST ELEMENT {i+1} - Classes: {post.get('class', [])}")
            print(f"{'='*60}")

            # Pega o h2 e p que estão em post
            h2s = post.find_all('h2', recursive=True)
            ps = post.find_all('p', recursive=True)
            for h2 in h2s:
                title_text = h2.get_text(strip=True)
                print(title_text)
                title = title_text
                # Pegar o link do post
                a = h2.find("a")
                if a and a.has_attr("href"):
                    link = a["href"]
                    full_link = f"https://www.serebii.net{link}"
                    print(full_link)
            for p in ps:
                p_text = p.get_text(strip=True)
                print(p_text)
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

if __name__ == "__main__":
    html = scraper_serebii()
    if html:
        print("\nSucesso! HTML obtido do Serebii.")
    else:
        print("\nFalha ao obter HTML.")