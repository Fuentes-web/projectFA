import { useState } from "react";
import { crearTransaccion } from "../api/api";

export default function TransactionForm({ onClose }) {
  const [form, setForm] = useState({
    descripcion: "",
    monto: "",
    tipo: "Ingreso",
    categoria: "Alimentación",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      descripcion: form.descripcion,
      monto: Number(form.monto),
      tipo: form.tipo,
      categoria: form.categoria,
    };

    await crearTransaccion(data);
    onClose();
    window.location.reload();
  };

  return (
    <div
      className="modal-backdrop show d-flex justify-content-center align-items-center"
      style={{ background: "rgba(0,0,0,0.5)", position: "fixed", inset: 0 }}
    >
      <div className="card shadow p-4" style={{ width: "500px" }}>
        <h3 className="mb-3">Nueva Transacción</h3>

        <form onSubmit={handleSubmit}>
          {/* Descripción */}
          <div className="mb-3">
            <label className="form-label">Descripción</label>
            <input
              type="text"
              name="descripcion"
              className="form-control"
              onChange={handleChange}
              required
            />
          </div>

          {/* Monto */}
          <div className="mb-3">
            <label className="form-label">Monto</label>
            <input
              type="number"
              name="monto"
              className="form-control"
              onChange={handleChange}
              required
            />
          </div>

          {/* Tipo */}
          <div className="mb-3">
            <label className="form-label">Tipo</label>
            <select
              name="tipo"
              className="form-select"
              value={form.tipo}
              onChange={handleChange}
            >
              <option value="Ingreso">Ingreso</option>
              <option value="Gasto">Gasto</option>
            </select>
          </div>

          {/* Categoría */}
          <div className="mb-3">
            <label className="form-label">Categoría</label>
            <select
              name="categoria"
              className="form-select"
              value={form.categoria}
              onChange={handleChange}
            >
              <option value="Alimentación">Alimentación</option>
              <option value="Hogar">Hogar</option>
              <option value="Transporte">Transporte</option>
              <option value="Entretenimiento">Entretenimiento</option>
              <option value="Salud">Salud</option>
              <option value="Otros">Otros</option>
              <option value="Trabajo">Trabajo</option>
              <option value="Educación">Educación</option>
            </select>
          </div>

          {/* BOTONES */}
          <div className="d-flex justify-content-end gap-2">
            <button type="submit" className="btn btn-primary">
              Guardar
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
            >
              Cancelar
            </button> 
          </div>
        </form>
      </div>
    </div>
  );
}
