import { useEffect, useState } from "react";
import { fetchTransacciones } from "../api/api";
import BarChartCategorias from "../components/BarChartCategorias";
import PieGastos from "../components/PieGastos";
import LineIngresosGastos from "../components/LineIngresosGastos";

export default function Dashboard() {
  const [tx, setTx] = useState([]);

  useEffect(() => {
    fetchTransacciones().then(setTx);
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      
      <h3>Gastos por categoría</h3>
      <BarChartCategorias tx={tx} />

      <h3>Distribución de gastos</h3>
      <PieGastos tx={tx} />

      <h3>Ingresos vs Gastos por mes</h3>
      <LineIngresosGastos tx={tx} />
    </div>
  );
}
