# Required installation
# Run this command in your environment to install the required packages:
# pip install flask pandas keras pillow matplotlib sentinelhub
import os
import time
from keras.layers import LeakyReLU
from flask import Flask, request, jsonify
import pandas as pd
from PIL import Image
from keras.models import load_model
import numpy as np
import requests
from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubRequest,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType,
)

import matplotlib.pyplot as plt

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained model (ensure your model is loaded properly here)
model = load_model(
    r"wildfire\assets\model2.h5", custom_objects={"LeakyReLU": LeakyReLU}
)  # Update this path to your model


# Helper function to fetch and process the last available moisture image
def fetch_last_available_image(lat, long, height=0.01221, width=0.02315, resolution=10):
    """
    Fetch and process the last available moisture image for a specified location.

    Parameters:
        lat (float): Latitude of the center of the area of interest.
        long (float): Longitude of the center of the area of interest.
        height (float): Height of the bounding box in degrees. Default is 0.01221.
        width (float): Width of the bounding box in degrees. Default is 0.02315.
        resolution (int): Spatial resolution in meters. Default is 10.

    Returns:
        np.ndarray: Processed image array of shape (1, 300, 430, 3).
    """
    # Configuration
    config = SHConfig()
    config.sh_client_id = "sh-2145f7f9-3df8-4947-9f81-5c21fd628701"
    config.sh_client_secret = "FDgImn3CfZGeRSY1pbGu1kmug8FWsJrU"
    config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    config.sh_base_url = "https://sh.dataspace.copernicus.eu"
    config.save("cdse")

    # Define Area of Interest (AOI)
    aoi_coords_wgs84 = [
        long - width / 2,
        lat - height / 2,
        long + width / 2,
        lat + height / 2,
    ]

    aoi_bbox = BBox(bbox=aoi_coords_wgs84, crs=CRS.WGS84)
    aoi_size = bbox_to_dimensions(aoi_bbox, resolution=resolution)

    # Evalscript for Moisture Image
    evalscript_moisture = """
    //VERSION=3
    const moistureRamps = [
      [-0.8, 0x800000],
      [-0.24, 0xff0000],
      [-0.032, 0xffff00],
      [0.032, 0x00ffff],
      [0.24, 0x0000ff],
      [0.8, 0x000080],
    ];

    const viz = new ColorRampVisualizer(moistureRamps);

    function setup() {
      return {
        input: ["B03", "B04", "B8A", "B11", "dataMask"],
        output: [
          { id: "default", bands: 4 },
          { id: "index", bands: 1, sampleType: "FLOAT32" },
          { id: "eobrowserStats", bands: 2, sampleType: "FLOAT32" },
          { id: "dataMask", bands: 1 },
        ],
      };
    }

    function evaluatePixel(samples) {
      let val = index(samples.B8A, samples.B11);
      return {
        default: [...viz.process(val), samples.dataMask],
        index: [val],
        eobrowserStats: [val, 0],
        dataMask: [samples.dataMask],
      };
    }
    """

    # Request for last available moisture image
    request_moisture = SentinelHubRequest(
        evalscript=evalscript_moisture,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A.define_from(
                    name="s2l2a", service_url="https://sh.dataspace.copernicus.eu"
                ),
                time_interval=("2022-01-01", "2023-01-01"),
                other_args={"dataFilter": {"mosaickingOrder": "leastCC"}},
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=aoi_bbox,
        size=aoi_size,
        config=config,
    )

    # Get data
    moisture_imgs = request_moisture.get_data()

    if moisture_imgs:
        image = moisture_imgs[0]
        if len(image.shape) == 3 and image.shape[2] == 4:
            # Drop the alpha channel if present
            image = image[:, :, :3]
        image = Image.fromarray(image.astype("uint8"))  # Ensure array is uint8
        image = image.resize((430, 300))  # Resize the image
        image_array = np.array(image) / 255.0  # Normalize the image
        return np.expand_dims(image_array, axis=0)  # Add batch dimension

    else:
        raise ValueError("No images available for the specified location.")


def fetch_weather_data(lat, long):
    """
    Fetch weather data for a specified latitude and longitude.

    Parameters:
        lat (float): Latitude of the location.
        long (float): Longitude of the location.

    Returns:
        dict: Extracted weather data (pressure, humidity, temp, wind_speed, wind_deg, clouds).
    """
    # Get timestamp for yesterday at 14:00
    current_time = int(time.time())
    from datetime import datetime, timedelta

    # Get timestamp for yesterday at 14:00
    yesterday = datetime.now() - timedelta(days=1)
    target_time = yesterday.replace(hour=14, minute=0, second=0, microsecond=0)
    timestamp = int(target_time.timestamp())  # Subtract 24 hours in seconds

    # OpenWeather API URL
    api_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={long}&dt={timestamp}&units=metric&appid=b129e0aeb7cf77babab6419836b3c956"

    # Make the API request
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        # Extract needed information
        weather = data["data"][0]  # Use the first available data point
        return {
            "pressure": weather["pressure"],
            "humidity": weather["humidity"],
            "temp": weather["temp"],
            "wind_speed": weather["wind_speed"],
            "wind_deg": weather["wind_deg"],
            "clouds": weather["clouds"],
        }
    else:
        raise ValueError(
            f"Failed to fetch weather data: {response.status_code} {response.text}"
        )


# Define the endpoint
@app.route("/predict_wildfire_risk", methods=["POST"])
def predict_wildfire_risk():
    try:

        lat = float(request.form["lat"])
        long = float(request.form["long"])

        # Create a dictionary and ensure correct order of the data
        # Fetch weather data from OpenWeather API
        weather_data = fetch_weather_data(lat, long)

        # Convert weather data to a NumPy array with correct shape
        tabular_array = np.array([list(weather_data.values())])  # Shape (1, 6)

        # Fetch and process the image using the specified latitude and longitude
        image_array = fetch_last_available_image(lat, long)  # Get processed image array

        # Prepare inputs for the model
        model_inputs = [
            image_array,
            tabular_array,
        ]  # Ensure correct order: image first, tabular second

        # Make predictions
        prediction = model.predict(model_inputs)

        # Respond with the prediction
        return jsonify({"wildfire_risk_prediction": float(round(prediction[0][0], 3))})

    except Exception as e:
        return jsonify({"error": str(e)})


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
