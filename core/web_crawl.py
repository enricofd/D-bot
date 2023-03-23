import requests
from bs4 import BeautifulSoup
import re

def crawl(urls: list) -> list:
    
    search_urls = set(urls)
    searched_urls = set()
    result = []
    actual_depth = 0

    while actual_depth <= 1:
        depth_urls = set()
        
        for url in search_urls:
            
            try:
                res = requests.get(url)
                html_page = res.text
                searched_urls.add(url)

                soup = BeautifulSoup(html_page, 'html.parser')
                title = soup.title.string
                text = soup.get_text()
                result.append((title, text))

                if actual_depth < 1:
                    for link in soup.findAll('a', attrs={'href': re.compile("http.+")}):
                        depth_urls.add(link.get('href'))
                            
            except:
                pass

        search_urls = depth_urls
        actual_depth += 1

        print("done", searched_urls)

    return searched_urls, result

    