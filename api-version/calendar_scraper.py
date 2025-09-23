import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
TE_API_KEY = os.getenv("TE_API_KEY")

def fetch_forex_factory_events():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    table = soup.find("table", {"id": "calendar__table"})
    if not table:
        return []
    events = []
    rows = table.find_all("tr", class_="calendar__row")
    for row in rows:
        try:
            events.append({
                "time": row.find("td", class_="calendar__time").get_text(strip=True),
                "currency": row.find("td", class_="calendar__currency").get_text(strip=True),
                "impact": row.find("td", class_="calendar__impact").find("span")["title"],
                "event": row.find("td", class_="calendar__event").get_text(strip=True),
                "actual": row.find("td", class_="calendar__actual").get_text(strip=True),
                "forecast": row.find("td", class_="calendar__forecast").get_text(strip=True),
                "previous": row.find("td", class_="calendar__previous").get_text(strip=True)
            })
        except:
            continue
    return events

def fetch_investing_calendar():
    url = "https://www.investing.com/economic-calendar/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    rows = soup.select("tr.js-event-item")
    events = []
    for row in rows:
        try:
            events.append({
                "time": row.select_one(".first.left.time").get_text(strip=True),
                "currency": row.select_one(".left.flagCur.noWrap").get_text(strip=True),
                "impact": row.select_one(".sentiment span")["title"],
                "event": row.select_one(".event").get_text(strip=True),
                "actual": row.select_one(".act").get_text(strip=True),
                "forecast": row.select_one(".fore").get_text(strip=True),
                "previous": row.select_one(".prev").get_text(strip=True)
            })
        except:
            continue
    return events

def fetch_tradingeconomics_calendar():
    if not TE_API_KEY:
        return [{"error": "Missing TradingEconomics API key"}]
    url = f"https://api.tradingeconomics.com/calendar?c={TE_API_KEY}&f=json"
    try:
        res = requests.get(url)
        data = res.json()
        events = []
        for item in data[:50]:
            events.append({
                "country": item.get("Country"),
                "event": item.get("Event"),
                "date": item.get("Date"),
                "actual": item.get("Actual"),
                "forecast": item.get("Forecast"),
                "previous": item.get("Previous"),
                "importance": item.get("Importance")
            })
        return events
    except Exception as e:
        return [{"error": str(e)}]
