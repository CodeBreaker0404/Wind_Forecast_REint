export function applyForecastHorizon(data, horizon) {

  return data.map(row => {

    if (row.generation_forecast === null) {
      return row;
    }

    // simulate horizon filtering
    const forecastValue = row.generation_forecast;

    const adjustedForecast =
      horizon > 0 ? forecastValue - (horizon * 5) : forecastValue;

    return {
      ...row,
      generation_forecast: adjustedForecast
    };

  });

}