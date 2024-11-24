export const metersToDegrees = (meters, latitude) => {
  const earthCircumference = 40075017; // Earth's circumference in meters
  const degreesPerMeter = 360 / earthCircumference;
  const latitudeAdjustment = degreesPerMeter;
  const longitudeAdjustment =
    degreesPerMeter / Math.cos(latitude * (Math.PI / 180));
  return {
    lat: meters * latitudeAdjustment,
    lng: meters * longitudeAdjustment,
  };
};

export const getScaledColor = (riskValue) => {
  const clampedValue = Math.max(0, Math.min(1, riskValue));
  const red = Math.floor(255 * clampedValue);
  const green = Math.floor(255 * (1 - clampedValue));
  return `rgb(${red},${green},0)`;
};
