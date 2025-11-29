import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

export default function LineIngresosGastos({ tx }) {
  const monthly = {};

  tx.forEach(t => {
    const m = new Date(t.fecha).toISOString().slice(0,7); // YYYY-MM
    if (!monthly[m]) monthly[m] = { mes: m, ingreso: 0, gasto: 0 };

    if (t.tipo === "Ingreso") monthly[m].ingreso += t.monto;
    else monthly[m].gasto += t.monto;
  });

  const data = Object.values(monthly);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="mes" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="ingreso" stroke="#28a745" />
        <Line type="monotone" dataKey="gasto" stroke="#dc3545" />
      </LineChart>
    </ResponsiveContainer>
  );
}
