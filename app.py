from flask import Flask, jsonify
from flask_cors import CORS

from scraper import scrape_all


app = Flask(__name__)
CORS(app)


# -------------------------------
# HOME ROUTE
# -------------------------------

@app.route("/")
def home():

    return jsonify({
        "status": "Indian Commodities API Running",
        "endpoints": {
            "/api/metals": "Get all commodities",
            "/api/metals/<name>": "Get specific commodity"
        }
    })


# -------------------------------
# ALL COMMODITIES
# -------------------------------

@app.route("/api/metals")
def get_all():

    data = scrape_all()

    return jsonify(data)


# -------------------------------
# SINGLE COMMODITY
# -------------------------------

@app.route("/api/metals/<name>")
def get_one(name):

    data = scrape_all()

    name = name.lower()

    if name in data:
        return jsonify(data[name])

    return jsonify({"error": "Commodity not found"}), 404


# -------------------------------
# RUN SERVER
# -------------------------------

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
