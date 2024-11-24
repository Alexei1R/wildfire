from flask import Flask, request, jsonify
import random
from flask_cors import CORS
import time 
app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route('/predict_wildfire_risk', methods=['GET'])
def predict_wildfire_risk():
    # Get parameters from request
    lat = request.args.get('lat', type=float)
    long = request.args.get('long', type=float)

    print(f"Lat {lat} , Long {long}")
    time.sleep(1)
    # Validate parameters
    if lat is None or long is None:
        return jsonify({"error": "Missing required parameters 'lat' and 'long'"}), 400

    # Generate a random float between 0 and 1
    risk_score = random.uniform(0, 1)

    # Return the result as JSON
    return jsonify({
        "wildfire_risk_score": risk_score
    })

if __name__ == '__main__':
    app.run(port=8005)
