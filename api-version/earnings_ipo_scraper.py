import requests
from bs4 import BeautifulSoup

def fetch_nasdaq_earnings():
    url = "https://www.nasdaq.com/market-activity/earnings"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    earnings = []
    rows = soup.select(".calendar__row")
    for row in rows[:10]:
        try:
            earnings.append({
                "ticker": row.find("a").get_text(strip=True),
                "company": row.select_one(".calendar__company-name").get_text(strip=True),
                "time": row.select_one(".calendar__time").get_text(strip=True),
                "date": row.select_one(".calendar__date").get_text(strip=True)
            })
        except:
            continue
    return earnings

def fetch_nasdaq_ipos():
    url = "https://www.nasdaq.com/market-activity/ipos"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    ipos = []
    rows = soup.select("table tr")[1:]
    for row in rows[:10]:
        try:
            cols = row.find_all("td")
            ipos.append({
                "company": cols[0].get_text(strip=True),
                "symbol": cols[1].get_text(strip=True),
                "expected_date": cols[2].get_text(strip=True),
                "price_range": cols[3].get_text(strip=True),
                "shares": cols[4].get_text(strip=True)
            })
        except:
            continue
    return ipos
