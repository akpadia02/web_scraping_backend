from flask import Flask, jsonify
from flask_cors import CORS
from scraper import scrape_bullions
import time

app = Flask(__name__)
CORS(app)

cache_data = {}
last_updated = 0
CACHE_INTERVAL = 180   # seconds

def get_metals_data():
    global cache_data, last_updated
    now = time.time()
    if now - last_updated > CACHE_INTERVAL:
        try:
            cache_data = scrape_bullions()
            last_updated = now
        except Exception as e:
            print("Scraping error:", e)
            cache_data = {"error": str(e)}
    return cache_data

@app.route("/api/metals")
def metals():
    return jsonify(get_metals_data())

@app.route("/api/metals/<metal_name>")
def get_metal(metal_name):
    """Get specific metal price"""
    all_metals = get_metals_data()
    metal = all_metals.get(metal_name.lower())
    if metal:
        return jsonify({metal_name.lower(): metal})
    return jsonify({"error": f"{metal_name} not found"}), 404

@app.route("/")
def home():
    return jsonify({
        "status": "Indian Metals API Running",
        "endpoints": {
            "/api/metals": "Get all metals prices",
            "/api/metals/<metal>": "Get specific metal price"
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
