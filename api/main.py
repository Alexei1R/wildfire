# Utilities
import matplotlib.pyplot as plt
import numpy as np
import getpass

from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubRequest,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType,
)

# Configuration
config = SHConfig()
config.sh_client_id = "sh-2145f7f9-3df8-4947-9f81-5c21fd628701"
config.sh_client_secret = "FDgImn3CfZGeRSY1pbGu1kmug8FWsJrU"
config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
config.sh_base_url = "https://sh.dataspace.copernicus.eu"
config.save("cdse")

latlong_center= [41.23504, 25.9001]
# Area of Interest from the center +- 0.05985 in vertical and horizontal +- 0.01163
aoi_coords_wgs84 = [latlong_center[1]-0.01163, latlong_center[0]-0.05985, latlong_center[1]+0.01163, latlong_center[0]+0.05985]


resolution = 10
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
  // The library for tiffs works well only if there is only one channel returned.
  // So we encode the "no data" as NaN here and ignore NaNs on frontend.
  const indexVal = samples.dataMask === 1 ? val : NaN;
  return {
    default: [...viz.process(val), samples.dataMask],
    index: [indexVal],
    eobrowserStats: [val, isCloud(samples) ? 1 : 0],
    dataMask: [samples.dataMask],
  };
}

function isCloud(samples) {
  const NGDR = index(samples.B03, samples.B04);
  const bRatio = (samples.B03 - 0.175) / (0.39 - 0.175);
  return bRatio > 1 || (bRatio > 0 && NGDR > 0);
}
"""

# Request for Moisture Image
request_moisture = SentinelHubRequest(
    evalscript=evalscript_moisture,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L2A.define_from(
                name="s2l2a", service_url="https://sh.dataspace.copernicus.eu"
            ),
            time_interval=("2022-05-01", "2022-05-20"),
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

# Display the image
image = moisture_imgs[0]
plt.figure(figsize=(10, 10))
plt.imshow(np.clip(image / 255., 0, 1))
plt.axis('off')
plt.show()
