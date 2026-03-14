import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function ForecastChart({ data }) {

  return (
    <ResponsiveContainer width="100%" height={450}>
      <LineChart data={data}>

        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="startTime"
          tickFormatter={(t) =>
            new Date(t).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit"
            })
          }
          minTickGap={40}
        />

        <YAxis
          label={{ value: "Power (MW)", angle: -90, position: "insideLeft" }}
        />

        <Tooltip
          formatter={(value) => `${Math.round(value)} MW`}
        />

        <Legend />

        <Line
          type="monotone"
          dataKey="generation_actual"
          stroke="#1976d2"
          strokeWidth={2}
          dot={false}
          name="Actual Generation"
        />

        <Line
          type="monotone"
          dataKey="generation_forecast"
          stroke="#2e7d32"
          strokeWidth={2}
          dot={false}
          name="Forecast Generation"
          connectNulls={true}
        />

      </LineChart>
    </ResponsiveContainer>
  );
}