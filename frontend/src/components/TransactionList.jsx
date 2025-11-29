import { useEffect, useState } from "react";
import { fetchTransacciones } from "../api/api";

export default function TransactionList({ filters }) {
  const [tx, setTx] = useState([]);

  useEffect(() => {
    fetchTransacciones(filters).then(setTx);
  }, [filters]);

  return (
    <table className="tabla">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Descripción</th>
          <th>Monto</th>
          <th>Tipo</th>
          <th>Categoría</th>
        </tr>
      </thead>
      <tbody>
        {tx.map(t => (
          <tr key={t.id}>
            <td>{new Date(t.fecha).toLocaleString()}</td>
            <td>{t.descripcion}</td>
            <td>{t.monto}</td>
            <td>{t.tipo}</td>
            <td>{t.categoria}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
