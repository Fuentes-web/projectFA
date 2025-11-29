import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function BarChartCategorias({ tx }) {
  const data = [];

  tx.forEach(t => {
    if (t.tipo === "Gasto") {
      const cat = data.find(d => d.categoria === t.categoria);
      if (cat) cat.monto += t.monto;
      else data.push({ categoria: t.categoria, monto: t.monto });
    }
  });

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <XAxis dataKey="categoria" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="monto" fill="#d9534f" />
      </BarChart>
    </ResponsiveContainer>
  );
}
