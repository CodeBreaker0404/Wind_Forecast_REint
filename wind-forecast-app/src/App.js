import React, { useState, useEffect } from "react";
import { Container, Typography, Card, CardContent, Grid } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";

import { applyForecastHorizon } from "./services/horizonService";
import Controls from "./components/Controls";
import ForecastChart from "./components/ForecastChart";
import { loadWindData } from "./services/dataService";

function App() {

  const [startTime, setStartTime] = useState(dayjs("2024-01-01T00:00"));
  const [endTime, setEndTime] = useState(dayjs("2024-01-02T00:00"));
  const [horizon, setHorizon] = useState(4);

  const [rawData, setRawData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [loading, setLoading] = useState(true);

  // load dataset once
  useEffect(() => {
    loadWindData().then((data) => {
      setRawData(data);
      setFilteredData(data);
      setLoading(false);
    });
  }, []);

  // filter data when time or horizon changes
  useEffect(() => {

    const filtered = rawData.filter((row) => {
      const t = dayjs(row.startTime);
      return (
        t.isSame(startTime) ||
        t.isSame(endTime) ||
        (t.isAfter(startTime) && t.isBefore(endTime))
      );
    });

    const horizonAdjusted = applyForecastHorizon(filtered, horizon);

    setFilteredData(horizonAdjusted);

  }, [rawData, startTime, endTime, horizon]);

  /* ---------- Metrics ---------- */

  const avgGeneration =
    filteredData.length > 0
      ? filteredData.reduce((sum, r) => sum + r.generation_actual, 0) /
        filteredData.length
      : 0;

  const maxGeneration =
    filteredData.length > 0
      ? Math.max(...filteredData.map((r) => r.generation_actual))
      : 0;

  const minGeneration =
    filteredData.length > 0
      ? Math.min(...filteredData.map((r) => r.generation_actual))
      : 0;

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>

      <Container maxWidth="lg" sx={{ marginTop: 4, marginBottom: 4 }}>

        {/* Dashboard Title */}
        <Typography variant="h4" gutterBottom>
          UK Wind Power Forecast Monitoring
        </Typography>

        <Typography variant="body1" color="text.secondary" sx={{ marginBottom: 3 }}>
          Compare actual wind generation with forecasted values and analyze forecast performance over time.
        </Typography>

        {/* Controls */}
        <Controls
          startTime={startTime}
          setStartTime={setStartTime}
          endTime={endTime}
          setEndTime={setEndTime}
          horizon={horizon}
          setHorizon={setHorizon}
        />

        {/* Metrics */}
        <Grid container spacing={2} sx={{ marginTop: 2 }}>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">
                  Average Generation
                </Typography>
                <Typography variant="h6">
                  {Math.round(avgGeneration)} MW
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">
                  Maximum Generation
                </Typography>
                <Typography variant="h6">
                  {Math.round(maxGeneration)} MW
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" color="text.secondary">
                  Minimum Generation
                </Typography>
                <Typography variant="h6">
                  {Math.round(minGeneration)} MW
                </Typography>
              </CardContent>
            </Card>
          </Grid>

        </Grid>

        {/* Chart Card */}
        <Card sx={{ marginTop: 4 }}>
          <CardContent>

            {loading ? (
              <Typography>Loading wind generation data...</Typography>
            ) : (
              <ForecastChart data={filteredData} />
            )}

          </CardContent>
        </Card>

      </Container>

    </LocalizationProvider>
  );
}

export default App;