from flask import Flask, jsonify
from calendar_scraper import (
    fetch_forex_factory_events,
    fetch_investing_calendar,
    fetch_tradingeconomics_calendar
)
from news_fetcher import fetch_reuters_news, fetch_yahoo_finance_news
from earnings_ipo_scraper import fetch_nasdaq_earnings, fetch_nasdaq_ipos

app = Flask(__name__)

@app.route('/economic-calendar')
def economic_calendar():
    combined = (
        fetch_forex_factory_events()
        + fetch_investing_calendar()
        + fetch_tradingeconomics_calendar()
    )
    return jsonify(combined)

@app.route('/market-news')
def market_news():
    return jsonify(fetch_reuters_news() + fetch_yahoo_finance_news())

@app.route('/earnings-calendar')
def earnings_calendar():
    return jsonify(fetch_nasdaq_earnings())

@app.route('/ipo-calendar')
def ipo_calendar():
    return jsonify(fetch_nasdaq_ipos())

if __name__ == '__main__':
    app.run(debug=True)
