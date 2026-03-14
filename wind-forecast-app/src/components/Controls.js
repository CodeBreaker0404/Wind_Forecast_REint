import React from "react";
import { Grid, Slider, Typography } from "@mui/material";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";

export default function Controls({
  startTime,
  setStartTime,
  endTime,
  setEndTime,
  horizon,
  setHorizon
}) {
  return (
    <Grid container spacing={3} alignItems="center">

      {/* Start Time */}
      <Grid item xs={12} md={4}>
        <Typography variant="subtitle2">Start Time</Typography>

        <DateTimePicker
          value={startTime}
          onChange={(newValue) => setStartTime(newValue)}
          slotProps={{ textField: { fullWidth: true } }}
        />
      </Grid>

      {/* End Time */}
      <Grid item xs={12} md={4}>
        <Typography variant="subtitle2">End Time</Typography>

        <DateTimePicker
          value={endTime}
          onChange={(newValue) => setEndTime(newValue)}
          slotProps={{ textField: { fullWidth: true } }}
        />
      </Grid>

      {/* Horizon Slider */}
      <Grid item xs={12} md={4}>
        <Typography variant="subtitle2">
          Forecast Horizon: {horizon} hours
        </Typography>

        <Slider
          value={horizon}
          min={0}
          max={48}
          step={1}
          valueLabelDisplay="auto"
          onChange={(e, val) => setHorizon(val)}
        />
      </Grid>

    </Grid>
  );
}