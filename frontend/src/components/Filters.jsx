import { useState } from "react";

export default function Filters({ onChange }) {
  const [categoria, setCategoria] = useState("");
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");

  const actualizar = () => {
    onChange({
      categoria: categoria || undefined,
      desde: desde || undefined,
      hasta: hasta || undefined,
    });
  };

  return (
    <div className="filtros">
      <select value={categoria} onChange={e => setCategoria(e.target.value)}>
        <option value="">Todas</option>
        <option value="Alimentación">Alimentación</option>
        <option value="Hogar">Hogar</option>
        <option value="Transporte">Transporte</option>
        <option value="Entretenimiento">Entretenimiento</option>
        <option value="Salud">Salud</option>
        <option value="Trabajo">Trabajo</option>
        <option value="Educación">Educación</option>
        <option value="Otros">Otros</option>
      </select>

      <input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
      <input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />

      <button onClick={actualizar}>Aplicar filtros</button>
    </div>
  );
}
