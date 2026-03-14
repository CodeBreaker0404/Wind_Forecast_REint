import requests
import pandas as pd
from datetime import datetime

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────
BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR"

# Wide publish window to capture all possible forecasts that cover Jan 2024
# Adjust wider if you miss data; narrower if you want to reduce volume
PUBLISH_FROM = "2023-12-20T00:00:00Z"   # ~10–12 days before Jan 1
PUBLISH_TO   = "2024-02-10T00:00:00Z"   # a few days after Jan 31

# Target period we actually care about (startTime in this range)
TARGET_START = "2024-01-01T00:00:00Z"
TARGET_END   = "2024-01-31T23:59:59Z"

OUTPUT_CSV = "wind_forecast_jan2024.csv"

# ────────────────────────────────────────────────
from datetime import datetime, timedelta
import requests
import pandas as pd

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/WINDFOR"

def fetch_all_wind_forecasts():
    # Target publish window to capture forecasts that could cover Jan 2024
    overall_start = datetime(2023, 12, 20)
    overall_end   = datetime(2024,  2, 10)

    chunk_days = 6  # Safe under 7-day limit (inclusive)
    all_records = []

    current_start = overall_start
    page_count = 0

    print("Fetching wind forecast data in chunks (max 7 days per request)...")

    while current_start < overall_end:
        current_end = min(current_start + timedelta(days=chunk_days), overall_end)

        # Format with .000Z to be extra safe (though :00:00Z usually works too)
        from_str = current_start.strftime("%Y-%m-%dT00:00:00.000Z")
        to_str   = current_end.strftime(  "%Y-%m-%dT23:59:59.999Z")  # inclusive end

        params = {
            "publishDateTimeFrom": from_str,
            "publishDateTimeTo":   to_str,
            "format": "json"
        }

        print(f"  Chunk: {from_str} → {to_str}")

        url = BASE_URL
        while url:
            page_count += 1
            try:
                r = requests.get(url, params=params, timeout=30)
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"Error on chunk {from_str}: {e}")
                if r.text:
                    print("Response:", r.text)
                return []  # or continue / raise depending on preference

            js = r.json()
            page_data = js.get("data", [])
            all_records.extend(page_data)

            next_url = js.get("next")
            if next_url:
                url = next_url
                params = None  # params only on first page
            else:
                url = None

        # Move to next chunk
        current_start = current_end + timedelta(days=1)  # +1 to avoid overlap/gap

    print(f"Finished. Total records downloaded: {len(all_records)}")
    return all_records


# ────────────────────────────────────────────────
# Then the rest stays almost the same:
data = fetch_all_wind_forecasts()

if not data:
    print("No data — check API status or widen/narrow chunks if needed.")
else:
    df = pd.DataFrame(data)
    df["publishTime"] = pd.to_datetime(df["publishTime"])
    df["startTime"]   = pd.to_datetime(df["startTime"])

    # Filter to Jan 2024 forecast periods
    jan_start = pd.Timestamp("2024-01-01T00:00:00Z")
    jan_end   = pd.Timestamp("2024-02-01T00:00:00Z")  # exclusive

    df_jan = df[(df["startTime"] >= jan_start) & (df["startTime"] < jan_end)].copy()

    if df_jan.empty:
        print("No Jan 2024 startTime records after filtering.")
        print("Try widening overall publish window (e.g. Dec 15 → Feb 15)")
    else:
        print(f"Found {len(df_jan)} forecast records for Jan 2024 periods")
        df_jan = df_jan.sort_values(["startTime", "publishTime"])
        df_jan[["startTime", "publishTime", "generation"]].to_csv(
            "wind_forecast_jan2024.csv", index=False
        )
        print("Saved wind_forecast_jan2024.csv")

# ────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────
data = fetch_all_wind_forecasts()

if not data:
    print("No data returned — check dates, API status or your internet.")
    exit()

df = pd.DataFrame(data)

# Ensure datetime columns
df["publishTime"] = pd.to_datetime(df["publishTime"])
df["startTime"]   = pd.to_datetime(df["startTime"])

# Filter to forecasts whose period falls (at least partially) in January 2024
# You can make this stricter: e.g. startTime >= TARGET_START & startTime < TARGET_END
mask = (df["startTime"] >= TARGET_START) & (df["startTime"] <= TARGET_END)
df_jan = df[mask].copy()

if df_jan.empty:
    print("No forecast records have startTime in January 2024.")
    print("Try widening the publishDateTimeFrom/To window further back/forward.")
else:
    print(f"Filtered to {len(df_jan)} forecast records covering Jan 2024")

    # Sort by startTime + publishTime (latest publish = most up-to-date forecast)
    df_jan = df_jan.sort_values(["startTime", "publishTime"])

    # Optional: keep only the latest forecast per startTime (most accurate)
    # df_jan_latest = df_jan.groupby("startTime").tail(1).reset_index(drop=True)

    # Save
    cols_to_save = ["startTime", "publishTime", "generation"]
    df_jan[cols_to_save].to_csv(OUTPUT_CSV, index=False)
    print(f"Saved to: {OUTPUT_CSV}")

    # Quick summary
    print("\nSample:")
    print(df_jan[["startTime", "publishTime", "generation"]].head(8))
    print("\nDate range of startTime in result:")
    print(df_jan["startTime"].min(), "→", df_jan["startTime"].max())