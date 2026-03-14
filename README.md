# Wind Power Forecast Monitoring Dashboard

## Overview

This project implements a **forecast monitoring dashboard for wind power generation in the United Kingdom**. The application allows users to visually compare **actual wind generation with forecasted generation** across different time ranges and forecast horizons.

The goal of the dashboard is to help users understand **forecast accuracy and variability in wind generation**, while also providing tools for analyzing forecast performance.

The project also includes a **data analysis notebook** that evaluates forecast errors and estimates reliable wind power availability.

---

## Features

### Forecast Monitoring Dashboard
The web application provides:

- Visualization of **actual wind generation vs forecasted generation**
- **Start and end time selection** using calendar controls
- **Forecast horizon adjustment** via an interactive slider
- Dynamic updates of the chart based on user selections
- Key statistics including:
  - Average generation
  - Maximum generation
  - Minimum generation

---

### Interactive Visualization

The dashboard includes:

- Responsive charts built with **Recharts**
- UI components using **Material UI**
- Forecast and actual generation displayed in a clear line chart
- Tooltips and gridlines for better readability

---

### Forecast Error Analysis

A Jupyter notebook (`analysis.ipynb`) analyzes forecast accuracy including:

- Mean forecast error
- Median forecast error
- P99 error
- Error distribution
- Variability of wind generation

---

## Tech Stack

### Frontend
- React
- Material UI
- Recharts
- DayJS

### Data Processing
- Python
- Pandas
- NumPy
- Matplotlib / Seaborn

### Deployment
- Vercel

---

## Project Structure

```
wind-forecast-dashboard
│
├── public/
│   └── processed_wind_dataset.json
│
├── src/
│   ├── components/
│   │   ├── Controls.js
│   │   └── ForecastChart.js
│   │
│   ├── services/
│   │   ├── dataService.js
│   │   └── horizonService.js
│   │
│   └── App.js
│
├── analysis.ipynb
├── processed_wind_dataset.csv
├── package.json
└── README.md
```

---

## Running the Application

### Install dependencies

```
npm install
```

### Start the development server

```
npm start
```

The application will run at:

```
http://localhost:3000
```

---

## Data Sources

Wind generation and forecast data are based on datasets provided by the **Elexon BMRS API**.

Documentation:  
https://bmrs.elexon.co.uk/api-documentation

Datasets used:

- **Actual Generation Dataset (FUELHH)**
- **Wind Forecast Dataset (WINDFOR)**

The datasets were processed and stored locally for visualization.

---

## Forecast Error Analysis

The analysis notebook evaluates the accuracy of wind power forecasts.

Key metrics computed include:

- **Mean Forecast Error**
- **Median Forecast Error**
- **P99 Forecast Error**

The analysis also examines wind generation variability and estimates a conservative level of wind power that can reliably contribute to electricity demand.

---

## AI Tool Usage

AI tools (ChatGPT) were used for:

- Debugging React components
- Structuring project architecture
- Improving UI components
- Assisting with interpretation of analysis results

All implementation decisions were verified and adapted manually.

---

## Author

**Akshar Samudrala**
