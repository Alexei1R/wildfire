// GridManager.js
import { useState } from "react";
import { metersToDegrees, getScaledColor } from "../utils/utils";

export const useGridManager = (map) => {
  const [gridSquares, setGridSquares] = useState([]);
  const [gridDrawn, setGridDrawn] = useState(false);

  const drawGrid = async () => {
    if (!map) return;

    // Clear existing grid squares
    gridSquares.forEach((square) => square.setMap(null));
    setGridSquares([]);

    const gridSize = 100;
    const paddingSize = 2;
    const maxSquares = 20;
    const centerLatLng = map.getCenter();
    const centerLat = centerLatLng.lat();
    const centerLng = centerLatLng.lng();

    const delta = metersToDegrees(gridSize, centerLat);
    const deltaPadding = metersToDegrees(paddingSize, centerLat);
    const totalGridWidth = (delta.lng + deltaPadding.lng) * maxSquares;
    const totalGridHeight = (delta.lat + deltaPadding.lat) * maxSquares;
    const startLat = centerLat - totalGridHeight / 2;
    const startLng = centerLng - totalGridWidth / 2;

    const newGridSquares = [];
    const promises = [];
    const concurrencyLimit = 10;
    let activeRequests = 0;
    let queue = [];

    const createSquare = async (lat, lng, delta, map) => {
      const centerLatSquare = lat + delta.lat / 2;
      const centerLngSquare = lng + delta.lng / 2;

      try {
        const response = await fetch(
          `http://127.0.0.1:8005/predict_wildfire_risk?lat=${centerLatSquare}&long=${centerLngSquare}`
        );
        const data = await response.json();
        const riskValue = data.wildfire_risk_score;

        const fillColor = getScaledColor(riskValue);
        const squareCoords = [
          { lat, lng },
          { lat: lat + delta.lat, lng },
          { lat: lat + delta.lat, lng: lng + delta.lng },
          { lat, lng: lng + delta.lng },
        ];

        const square = new window.google.maps.Polygon({
          paths: squareCoords,
          strokeColor: fillColor,
          strokeOpacity: 1.0,
          strokeWeight: 1,
          fillColor,
          fillOpacity: 0.5,
        });

        square.addListener("mouseover", () => square.setOptions({ fillOpacity: 0.8 }));
        square.addListener("mouseout", () => square.setOptions({ fillOpacity: 0.5 }));
        square.setMap(map);
        newGridSquares.push(square);
      } catch (error) {
        console.error("Error fetching risk value:", error);
      }
    };

    const wrappedCreateSquare = (lat, lng) => {
      return new Promise((resolve) => {
        const attempt = async () => {
          if (activeRequests < concurrencyLimit) {
            activeRequests++;
            await createSquare(lat, lng, delta, map);
            activeRequests--;
            resolve();
            if (queue.length > 0) queue.shift()();
          } else {
            queue.push(attempt);
          }
        };
        attempt();
      });
    };

    for (let row = 0; row < maxSquares; row++) {
      for (let col = 0; col < maxSquares; col++) {
        const lat = startLat + row * (delta.lat + deltaPadding.lat);
        const lng = startLng + col * (delta.lng + deltaPadding.lng);
        promises.push(wrappedCreateSquare(lat, lng));
      }
    }

    await Promise.all(promises);
    setGridSquares(newGridSquares);
    setGridDrawn(true);
  };

  return { drawGrid, gridDrawn };
};

