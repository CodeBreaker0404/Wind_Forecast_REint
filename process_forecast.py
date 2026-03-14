import pandas as pd
import json

# =========================
# Paths (update these)
# =========================
forecast_path = "wind_forecast_jan2024.csv"   # CSV with startTime, publishTime, generation
actual_path = "actual_wind_generation_jan2024.csv"       # CSV with startTime, generation_actual
output_path = "processed_wind_dataset"       # without extension, e.g. "./processed_wind_dataset"

# =========================
# Load data
# =========================
df_forecast = pd.read_csv(forecast_path)
df_actual = pd.read_csv(actual_path)

# =========================
# Convert timestamps
# =========================
df_forecast["startTime"] = pd.to_datetime(df_forecast["startTime"]).dt.tz_localize(None)
df_forecast["publishTime"] = pd.to_datetime(df_forecast["publishTime"]).dt.tz_localize(None)

df_actual["startTime"] = pd.to_datetime(df_actual["startTime"]).dt.tz_localize(None)

# =========================
# Compute forecast horizon (hours)
# =========================
df_forecast["horizon_hours"] = (
    (df_forecast["startTime"] - df_forecast["publishTime"]).dt.total_seconds() / 3600
)

# keep only valid horizons
df_forecast = df_forecast[
    (df_forecast["horizon_hours"] >= 0) &
    (df_forecast["horizon_hours"] <= 48)
]

# =========================
# Select latest forecast per startTime
# =========================
df_forecast = df_forecast.sort_values(["startTime", "publishTime"])

latest_forecast = df_forecast.groupby("startTime").tail(1)

latest_forecast = latest_forecast[["startTime", "generation"]]
latest_forecast.rename(columns={"generation": "generation_forecast"}, inplace=True)

# =========================
# Merge with actual generation
# =========================
df_final = pd.merge(
    df_actual,
    latest_forecast,
    on="startTime",
    how="left"
)

# =========================
# Save processed CSV
# =========================
csv_output = output_path + ".csv"
df_final.to_csv(csv_output, index=False)

print("CSV saved:", csv_output)

# =========================
# Convert to JSON
# =========================

df_final["startTime"] = df_final["startTime"].astype(str)
df_final = df_final.where(pd.notnull(df_final), None)

json_output = output_path + ".json"

# replace NaN with None
df_final = df_final.where(pd.notnull(df_final), None)

records = df_final.to_dict(orient="records")

with open(json_output, "w") as f:
    json.dump(records, f, indent=2)

print("JSON saved:", json_output)

# =========================
# Quick stats
# =========================
print("Rows:", len(df_final))
print("Forecast available:", df_final["generation_forecast"].notna().sum())