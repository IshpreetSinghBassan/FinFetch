from flask import Flask, jsonify
import logging
from calendar_scraper import (
    fetch_forex_factory_events,
    fetch_investing_calendar,
    fetch_tradingeconomics_calendar
)
from news_fetcher import fetch_reuters_news, fetch_yahoo_finance_news
from earnings_ipo_scraper import fetch_nasdaq_earnings, fetch_nasdaq_ipos

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "FinFetch API is running!",
        "endpoints": {
            "calendar": "/calendar - Get economic calendar events",
            "earnings_ipo": "/earnings-ipo - Get earnings and IPO data",
            "news": "/news - Get financial news"
        }
    })

@app.route('/calendar')
def calendar():
    try:
        logger.info("Fetching economic calendar data...")
        events = []
        
        # Try each source and combine results
        try:
            forex_events = fetch_forex_factory_events()
            events.extend(forex_events)
            logger.info(f"Fetched {len(forex_events)} events from Forex Factory")
        except Exception as e:
            logger.warning(f"Forex Factory failed: {str(e)}")
        
        try:
            investing_events = fetch_investing_calendar()
            events.extend(investing_events)
            logger.info(f"Fetched {len(investing_events)} events from Investing.com")
        except Exception as e:
            logger.warning(f"Investing.com failed: {str(e)}")
        
        try:
            te_events = fetch_tradingeconomics_calendar()
            events.extend(te_events)
            logger.info(f"Fetched {len(te_events)} events from TradingEconomics")
        except Exception as e:
            logger.warning(f"TradingEconomics failed: {str(e)}")
        
        return jsonify({
            "status": "success",
            "total_events": len(events),
            "data": events
        })
    
    except Exception as e:
        logger.error(f"Calendar endpoint error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to fetch calendar data",
            "error": str(e)
        }), 500

@app.route('/earnings-ipo')
def earnings_ipo():
    try:
        logger.info("Fetching earnings and IPO data...")
        
        earnings = []
        ipos = []
        
        try:
            earnings = fetch_nasdaq_earnings()
            logger.info(f"Fetched {len(earnings)} earnings reports")
        except Exception as e:
            logger.warning(f"Earnings fetch failed: {str(e)}")
        
        try:
            ipos = fetch_nasdaq_ipos()
            logger.info(f"Fetched {len(ipos)} IPOs")
        except Exception as e:
            logger.warning(f"IPO fetch failed: {str(e)}")
        
        return jsonify({
            "status": "success",
            "data": {
                "earnings": earnings,
                "ipos": ipos
            }
        })
    
    except Exception as e:
        logger.error(f"Earnings-IPO endpoint error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to fetch earnings/IPO data",
            "error": str(e)
        }), 500

@app.route('/news')
def news():
    try:
        logger.info("Fetching financial news...")
        articles = []
        
        try:
            reuters_articles = fetch_reuters_news()
            articles.extend(reuters_articles)
            logger.info(f"Fetched {len(reuters_articles)} articles from Reuters")
        except Exception as e:
            logger.warning(f"Reuters fetch failed: {str(e)}")
        
        try:
            yahoo_articles = fetch_yahoo_finance_news()
            articles.extend(yahoo_articles)
            logger.info(f"Fetched {len(yahoo_articles)} articles from Yahoo Finance")
        except Exception as e:
            logger.warning(f"Yahoo Finance fetch failed: {str(e)}")
        
        return jsonify({
            "status": "success",
            "total_articles": len(articles),
            "data": articles
        })
    
    except Exception as e:
        logger.error(f"News endpoint error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to fetch news data",
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": ["/calendar", "/earnings-ipo", "/news"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    import os
    import socket
    
    def find_free_port(start_port=5000):
        """Find a free port starting from start_port"""
        for port in range(start_port, start_port + 10):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', port))
                sock.close()
                return port
            except OSError:
                continue
        return start_port + 10  # Fallback
    
    # Try to use environment PORT, otherwise find a free one
    port = int(os.environ.get("PORT", 0))
    if port == 0:
        port = find_free_port(5000)
        logger.info(f"Port 5000 busy, using port {port} instead")
    
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    
    logger.info(f"Starting FinFetch API on port {port}")
    logger.info(f"Open your browser to: http://localhost:{port}")
    logger.info("Available endpoints:")
    logger.info(f"  - http://localhost:{port}/calendar")
    logger.info(f"  - http://localhost:{port}/earnings-ipo") 
    logger.info(f"  - http://localhost:{port}/news")
    
    try:
        app.run(host="0.0.0.0", port=port, debug=debug_mode)
    except OSError as e:
        if "Address already in use" in str(e):
            alternative_port = find_free_port(port + 1)
            logger.info(f"Port {port} busy, trying {alternative_port}")
            app.run(host="0.0.0.0", port=alternative_port, debug=debug_mode)
