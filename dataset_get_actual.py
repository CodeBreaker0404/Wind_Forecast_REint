import requests
import pandas as pd
from datetime import datetime, timedelta

# ────────────────────────────────────────────────
# CONFIG for ACTUAL WIND (FUELHH) - chunked
# ────────────────────────────────────────────────
FUELHH_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

# Target settlement period: full January 2024
overall_start_date = datetime(2024, 1, 1)
overall_end_date   = datetime(2024, 2, 1)   # exclusive end

chunk_days = 6  # Safe under 7-day inclusive limit

OUTPUT_ACTUAL_CSV = "actual_wind_generation_jan2024.csv"

# ────────────────────────────────────────────────
def fetch_actual_wind_chunk(start_date, end_date):
    """Fetch one chunk of settlement dates"""
    from_str = start_date.strftime("%Y-%m-%d")
    to_str   = end_date.strftime("%Y-%m-%d")

    params = {
        "settlementDateFrom": from_str,
        "settlementDateTo":   to_str,
        "fuelType":           "WIND",
        "format":             "json"
    }

    print(f"  Chunk: {from_str} → {to_str}")

    all_chunk_records = []
    url = FUELHH_URL

    while url:
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error in chunk {from_str}: {e}")
            if 'r' in locals() and r.text:
                print("Response:", r.text)
            return []

        js = r.json()
        page_data = js.get("data", [])
        all_chunk_records.extend(page_data)

        next_url = js.get("next")
        if next_url:
            url = next_url
            params = None
        else:
            url = None

    return all_chunk_records


# ────────────────────────────────────────────────
# MAIN - Fetch all chunks
# ────────────────────────────────────────────────
print("Fetching actual wind generation (FUELHH) for Jan 2024 in chunks...")

all_actual_data = []
current_start = overall_start_date

while current_start < overall_end_date:
    current_end = min(current_start + timedelta(days=chunk_days), overall_end_date)

    chunk_data = fetch_actual_wind_chunk(current_start, current_end)
    all_actual_data.extend(chunk_data)

    # Move to next chunk (add 1 day to avoid overlap/gap)
    current_start = current_end + timedelta(days=1)

print(f"Total records downloaded: {len(all_actual_data)} (expected ~1488 for Jan)")

if not all_actual_data:
    print("No data fetched. Check API status or try publishDateTime range instead.")
else:
    df_actual = pd.DataFrame(all_actual_data)

    # Clean up datetime
    df_actual["startTime"] = pd.to_datetime(df_actual["startTime"]).dt.tz_localize(None)

    # Keep essential columns
    df_actual = df_actual[["startTime", "generation"]].copy()
    df_actual.rename(columns={"generation": "generation_actual"}, inplace=True)

    # Sort and save
    df_actual = df_actual.sort_values("startTime")
    df_actual.to_csv(OUTPUT_ACTUAL_CSV, index=False)

    print(f"Saved {len(df_actual)} rows to {OUTPUT_ACTUAL_CSV}")

    # Summary
    print("\nDate range in data:", 
          df_actual["startTime"].min(), "→", df_actual["startTime"].max())
    print("Sample (first 6):")
    print(df_actual.head(6))