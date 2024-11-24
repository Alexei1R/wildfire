// GoogleMap.js
import React, { useEffect, useState } from "react";
import { useGridManager } from "./GridManager";

const GoogleMap = () => {
  const [map, setMap] = useState(null);
  const { drawGrid, gridDrawn } = useGridManager(map);

  useEffect(() => {
    const center = { lat: 47.02, lng: 28.86 };
    const mapInstance = new window.google.maps.Map(document.getElementById("map"), {
      center,
      zoom: 14,
      disableDefaultUI: true,
      draggable: true,
      mapTypeId: "satellite",
    });

    setMap(mapInstance);

    if (!window.google.maps.geometry) {
      console.error("Google Maps Geometry library is required.");
    }
  }, []);

  return (
    <div style={{ height: "100%", width: "100%", position: "relative" }}>
      <div id="map" style={{ height: "100%", width: "100%" }} />
      <button
        onClick={drawGrid}
        style={{
          position: "absolute",
          top: 10,
          left: 10,
          zIndex: 5,
          padding: "10px 20px",
          backgroundColor: "#007BFF",
          color: "#FFFFFF",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        {gridDrawn ? "Redraw Grid" : "Draw Grid"}
      </button>
    </div>
  );
};

export default GoogleMap;
