import requests
from bs4 import BeautifulSoup
import json

# proxy


key_words = {
    "london", "europe", "EUIC", "uk", "united kingdom", "england", "lisbon", "natural history museum", "excel center"
}

def scraper_serebii():
    serebii_url = "https://serebii.net/"

    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
    }

    try:
        print("Fazendo requisição...")

        response = requests.get(serebii_url, headers=HEADERS, proxies=proxy_config)
        response.raise_for_status()

        print(f"Status: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        # procura todos elementos com classe 'post'
        post_elements = soup.find_all(lambda tag: tag.has_attr('class') and 'post' in tag['class'])

        for i, post in enumerate(post_elements):
            print(f"\n{'='*60}")
            print(f"POST ELEMENT {i+1} - Classes: {post.get('class', [])}")
            print(f"{'='*60}")

            # pega o h2 e p que estão em post
            h2s = post.find_all('h2', recursive=True)
            ps = post.find_all('p', recursive=True)
            for h2 in h2s:
                print(f"h2: {h2.get_text(strip=True)}")
            for p in ps:
                print(f"p: {p.get_text(strip=True)}")

            # entra na div subcat de post 
            subcats = post.find_all(lambda tag: tag.has_attr('class') and 'subcat' in tag['class'])
            for j, subcat in enumerate(subcats):
                print(f"  {'-'*40}")
                print(f"  SUBCAT {j+1} inside POST {i+1} - Classes: {subcat.get('class', [])}")

                # pega o h3 e p que estão em subcat
                h3s = subcat.find_all('h3', recursive=True)
                subcat_ps = subcat.find_all('p', recursive=True)
                for h3 in h3s:
                    print(f"  h3: {h3.get_text(strip=True)}")
                for p in subcat_ps:
                    print(f"  p: {p.get_text(strip=True)}")
                print(f"  {'-'*40}")

                
            print(f"{'='*60}\n")

        return response.text
    
    except Exception as e:
        print(f"Erro: {e}")
        return None

if __name__ == "__main__":
    html = scraper_serebii()
    if html:
        print("\nSucesso! HTML obtido do Serebii.")
    else:
        print("\nFalha ao obter HTML.")