# 📊 FinFetch API

FinFetch is a RESTful API built with Python and Flask that provides aggregated **financial data**, including:

* 🌍 Global **economic calendar** events
* 💼 Upcoming **earnings reports** and **IPOs**
* 📰 Latest **financial and company news**

This API is ideal for financial apps, dashboards, or personal investment tools.

---

## 🚀 Features

* `GET /calendar`: Scrapes and returns upcoming macroeconomic events.
* `GET /earnings-ipo`: Fetches a list of earnings and IPOs from Nasdaq.
* `GET /news`: Aggregates real-time financial news from Yahoo Finance.

---

## 📁 Project Structure

```
.
├── app.py                  # Main Flask API routes
├── calendar_scraper.py    # Scraper for economic events
├── earnings_ipo_scraper.py# Scraper for earnings & IPOs
├── news_fetcher.py        # Yahoo Finance news fetcher
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python runtime version
├── render.yaml            # Render.com deployment config
└── README.md              # Project documentation
```

---

## 💪 How to Run Locally

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/your-username/finfetch.git
cd finfetch
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

API will run locally at: `http://127.0.0.1:5000`

---

## 🧪 API Endpoints

### `/calendar`

* **Method**: `GET`
* **Description**: Returns global economic events
* **Example Output**:

```json
[
  {
    "country": "United States",
    "event": "Nonfarm Payrolls",
    "actual": "272K",
    "forecast": "185K",
    "previous": "165K"
  }
]
```

---

### `/earnings-ipo`

* **Method**: `GET`
* **Description**: Returns upcoming earnings reports and IPOs.
* **Example Output**:

```json
{
  "earnings": ["Apple Inc. - 2024-07-25", "Tesla - 2024-07-26"],
  "ipos": ["NewTech IPO - 2024-07-28"]
}
```

---

### `/news`

* **Method**: `GET`
* **Description**: Returns trending financial news headlines.
* **Example Output**:

```json
[
  {
    "title": "Markets Rally Ahead of Fed Decision",
    "link": "https://finance.yahoo.com/..."
  }
]
```

---

## ☁️ Deploy to Render.com

This project includes a `render.yaml` file for easy deployment:

### Steps:

1. Push code to GitHub.
2. Log in to [Render](https://render.com/).
3. Click “New Web Service”.
4. Connect your GitHub repo.
5. It will auto-detect `render.yaml` and configure deployment.

---

## 🔧 Tech Stack

* Python 3.9
* Flask
* BeautifulSoup & Requests (for scraping)
* Hosted on Render (optional)

---

## 📄 License

Copyright (c) 2025 Ishpreet Bassan

All rights reserved.

Permission is hereby granted to any individual or organization ("User") to use, copy, modify, and distribute this software and its documentation, without fee, for **non-commercial** purposes only, provided that the above copyright notice and this permission notice appear in all copies of the software.

**Commercial Use:**

Commercial use, including reselling, sublicensing, integrating into paid services, or offering the software or services built with it as part of a commercial offering (e.g., SaaS platforms or APIs for which a subscription or fee is charged) is **strictly prohibited** without prior written permission or a separate commercial license agreement from the copyright holder.

If you wish to use this project commercially, you **must obtain a commercial license** by contacting:

> 📧 [ishpreetsingh08@yahoo.com](mailto:ishpreetsingh08@yahoo.com) 

This license is governed by and construed in accordance with the laws of \[Your Country].

---

**TL;DR:** Free for personal and educational use. Contact the author to use it commercially.
