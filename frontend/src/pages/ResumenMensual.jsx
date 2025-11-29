import { useEffect, useState } from "react";
import { fetchTransacciones } from "../api/api";

export default function ResumenMensual() {
  const [summary, setSummary] = useState([]);

  useEffect(() => {
    fetchTransacciones().then(tx => {
      const monthly = {};

      tx.forEach(t => {
        const m = new Date(t.fecha).toISOString().slice(0,7);
        if (!monthly[m]) monthly[m] = { mes: m, ingreso: 0, gasto: 0 };

        if (t.tipo === "Ingreso") monthly[m].ingreso += t.monto;
        else monthly[m].gasto += t.monto;
      });

      setSummary(Object.values(monthly));
    });
  }, []);

  return (
    <div>
      <h2>Resumen Mensual</h2>

      <table>
        <thead>
          <tr>
            <th>Mes</th>
            <th>Total Ingresos</th>
            <th>Total Gastos</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          {summary.map(s => (
            <tr key={s.mes}>
              <td>{s.mes}</td>
              <td>{s.ingreso}</td>
              <td>{s.gasto}</td>
              <td>{s.ingreso - s.gasto}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
