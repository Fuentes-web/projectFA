import { PieChart, Pie, Tooltip, Cell, ResponsiveContainer } from "recharts";

const COLORS = ["#FF6384","#36A2EB","#FFCE56","#4BC0C0","#9966FF","#FF9F40","#C12348"];

export default function PieGastos({ tx }) {
  const data = [];

  tx.forEach(t => {
    if (t.tipo === "Gasto") {
      const cat = data.find(d => d.name === t.categoria);
      if (cat) cat.value += t.monto;
      else data.push({ name: t.categoria, value: t.monto });
    }
  });

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" outerRadius={120}>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  );
}
