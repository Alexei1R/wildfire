
import matplotlib.pyplot as plt
import numpy as np
from sentinelhub import (
    SHConfig,
    DataCollection,
    SentinelHubRequest,
    BBox,
    bbox_to_dimensions,
    CRS,
    MimeType,
)


def fetch_last_available_image(lat, long, height=0.01221, width=0.02315, resolution=10):
    """
    Fetch and display the last available moisture image for a specified location.

    Parameters:
        lat (float): Latitude of the center of the area of interest.
        long (float): Longitude of the center of the area of interest.
        height (float): Height of the bounding box in degrees. Default is 0.01221.
        width (float): Width of the bounding box in degrees. Default is 0.02315.
        resolution (int): Spatial resolution in meters. Default is 10.

    Returns:
        None: Displays the image.
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
        # Display the image
        image = moisture_imgs[0]
        plt.figure(figsize=(10, 10))
        plt.imshow(np.clip(image / 255.0, 0, 1))
        plt.axis("off")
        plt.show()
    else:
        print("No images available for the specified location.")


fetch_last_available_image(47.02, 28.85)
