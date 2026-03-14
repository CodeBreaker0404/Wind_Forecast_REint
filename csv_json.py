import json
import math

input_path = "processed_wind_dataset.json"   # your current JSON file
output_path = "wind-forecast-app\public\processed_wind_dataset.json" # fixed JSON file

with open(input_path, "r") as f:
    data = json.load(f)

def replace_nan(obj):
    if isinstance(obj, dict):
        return {k: replace_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

data = replace_nan(data)

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print("NaN replaced with null and saved to", output_path)