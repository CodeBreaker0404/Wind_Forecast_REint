import axios from "axios";

export async function loadWindData() {
  const res = await axios.get("/processed_wind_dataset.json");
  return res.data;
}