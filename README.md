# Indian Metals Price API (Backend)

This is the backend service for the Indian Metals & Gold Price Dashboard.
It scrapes real-time gold prices from a reliable Indian source and exposes them via a REST API.

The backend is built using Python, Flask, and BeautifulSoup.

---

## Features

- Scrapes live gold prices (10K–24K)
- Provides REST API endpoint
- CORS enabled for frontend integration
- In-memory caching (no database required)
- Lightweight and fast
- Easy deployment on cloud platforms

---

## Tech Stack

| Technology    | Purpose              |
|---------------|----------------------|
| Python        | Backend Language     |
| Flask         | Web Framework        |
| Requests      | HTTP Client          |
| BeautifulSoup | Web Scraping         |
| Flask-CORS    | Cross-Origin Support |

---

## Project Structure

backend/
│
├── app.py
├── scraper.py
├── requirements.txt
└── README.md

---

## API Endpoint

### Get Metals Data

GET /api/metals

### Sample Response

{
  "gold": {
    "types": {
      "gold 24 karat": "15526",
      "gold 22 karat": "14232"
    },
    "unit": "INR/10g"
  }
}

---

## Installation & Setup (Local)

### Step 1: Clone Repository

git clone <your-repository-url>
cd indian-metals-dashboard/backend

### Step 2: Create Virtual Environment (Optional)

python -m venv venv
venv\Scripts\activate

### Step 3: Install Dependencies

pip install -r requirements.txt

### Step 4: Run Server

python app.py

Server will start at:

http://127.0.0.1:5000

---

## Testing the API

Open in browser:

http://127.0.0.1:5000/api/metals

Or using curl:

curl http://127.0.0.1:5000/api/metals

---

## Deployment

This backend can be deployed on:

- Render
- Railway
- PythonAnywhere
- Heroku

---

## Limitations

- Web scraping depends on website structure
- Free hosting may cause cold start delays
- Limited to precious metals currently

---

## Future Enhancements

- Add industrial metals support
- Automatic data refresh
- Price history tracking
- User authentication
- Live updates

---

## Author

Akshay H. Padia  
B.Tech CSE

---

## License

For academic and educational use only.
