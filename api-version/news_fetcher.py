import requests
from bs4 import BeautifulSoup

def fetch_reuters_news():
    url = "https://www.reuters.com/markets/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    for tag in soup.select("a.story-title, a[data-testid='Heading']")[:10]:
        text = tag.get_text(strip=True)
        link = "https://www.reuters.com" + tag.get("href")
        articles.append({"headline": text, "source": "Reuters", "url": link})
    return articles

def fetch_yahoo_finance_news():
    url = "https://finance.yahoo.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = []
    for tag in soup.select("h3 a")[:10]:
        text = tag.get_text(strip=True)
        link = "https://finance.yahoo.com" + tag.get("href")
        articles.append({"headline": text, "source": "Yahoo Finance", "url": link})
    return articles
