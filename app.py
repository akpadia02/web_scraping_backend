"""
================================================================================
FILE: app.py
RESPONSIBILITY: 
    Flask REST API server for Indian commodities market data.
    Handles HTTP requests and serves scraped commodity data (metals, oils, etc).
    Provides endpoints for retrieving all commodities or specific commodity data.
    Implements CORS for secure cross-origin requests from frontend.
================================================================================
"""

# Import Flask class for creating the web application
from flask import Flask, jsonify

# Import CORS to handle Cross-Origin Resource Sharing (allows frontend to access API)
from flask_cors import CORS

# Import the scraper function that retrieves and parses commodity data
from scraper import scrape_all


# Initialize Flask application instance
app = Flask(__name__)

# Enable CORS on all routes to allow requests from frontend on different origin
CORS(app)


# ============================================================================
# ROUTE: HOME / STATUS ENDPOINT
# ============================================================================
# PURPOSE: Provides API information and available endpoints
# RETURNS: JSON with status message and list of available endpoints

@app.route("/")
def home():
    # Return welcome message with endpoint information in JSON format
    return jsonify({
        "status": "Indian Commodities API Running",
        "endpoints": {
            "/api/metals": "Get all commodities",
            "/api/metals/<name>": "Get specific commodity"
        }
    })


# ============================================================================
# ROUTE: GET ALL COMMODITIES
# ============================================================================
# PURPOSE: Retrieves all commodity data (gold, silver, copper, crude oil, etc)
# RETURNS: JSON object containing all commodities with their market data

@app.route("/api/metals")
def get_all():
    # Call scraper function to fetch latest commodity data from source
    data = scrape_all()
    
    # Return scraped data as JSON response
    return jsonify(data)


# ============================================================================
# ROUTE: GET SINGLE COMMODITY
# ============================================================================
# PURPOSE: Retrieves data for a specific commodity by name
# PARAMETER: name - the name of the commodity (e.g., 'gold', 'silver')
# RETURNS: JSON with commodity data or 404 error if not found

@app.route("/api/metals/<name>")
def get_one(name):
    # Call scraper to fetch all commodity data
    data = scrape_all()
    
    # Convert search parameter to lowercase for case-insensitive matching
    name = name.lower()
    
    # Check if the requested commodity exists in the data
    if name in data:
        # Return the specific commodity data as JSON
        return jsonify(data[name])
    
    # Return error message if commodity not found with 404 status code
    return jsonify({"error": "Commodity not found"}), 404


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================
# PURPOSE: Starts the Flask development/production server
# HOST: 0.0.0.0 (accessible from any network interface)
# PORT: 5000 (standard Flask port)

if __name__ == "__main__":
    # Run the Flask application with server configuration
    app.run(host="0.0.0.0", port=5000)
