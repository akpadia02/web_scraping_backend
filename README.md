# Indian Metals Price API - Backend

Flask REST API for real-time precious metals pricing from bullions.co.in with intelligent caching.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Running](#running-the-application)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## Features

- Real-time precious metals price scraping
- RESTful API with CORS support
- 3-minute in-memory caching
- Graceful error handling
- Cloud-ready deployment

---

## Prerequisites

- Python 3.8+
- pip
- Internet connection

## Tech Stack

- Python 3.8+, Flask 3.1.2, BeautifulSoup4 4.14.3, Requests 2.32.5, flask-cors 6.0.2

---

## Installation

```bash
git clone <repo-url>
cd indian-metals-dashboard/backend
python -m venv venv
venv\\Scripts\\activate  # Windows: or source venv/bin/activate
pip install -r requirements.txt
python app.py  # Starts at http://127.0.0.1:5000
```

---

## API Documentation

**Base URLs:**
- Development: `http://127.0.0.1:5000`
- Production: `https://web-scraping-backend-k13b.onrender.com`

**Endpoints:**

`GET /` - API status

`GET /api/metals` - All metals prices
```json
{ "gold": { "types": { "gold 24 karat": "15526" }, "unit": "INR/10g" } }
```

`GET /api/metals/<metal>` - Specific metal (e.g., `/api/metals/gold`)

**Errors:** `{ "error": "Metal not found" }`

---

## Running the Application

```bash
# Development
python app.py

# Production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## Deployment

**Render:** Connect GitHub → Python environment → Start: `python app.py`

**Railway:** `railway login && railway up`

**Heroku:** `git push heroku main`

---

## Troubleshooting

**ModuleNotFoundError:** `pip install -r requirements.txt`

**Connection Error:** Check internet and firewall

**Port In Use:** Modify port in app.py

**Empty Response:** Website structure may have changed; update scraper.py

---

**Author:** Akshay H. Padia | B.Tech CSE


