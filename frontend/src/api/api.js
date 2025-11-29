const API_URL = "http://localhost:8000"; // <-- tu backend FastAPI

// Obtener transacciones con filtros
export async function fetchTransacciones(filters = {}) {
  const params = new URLSearchParams();

  if (filters.categoria) params.append("categoria", filters.categoria);
  if (filters.desde) params.append("desde", filters.desde);
  if (filters.hasta) params.append("hasta", filters.hasta);

  const url = `${API_URL}/transacciones?${params.toString()}`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Error obteniendo transacciones");

  return res.json();
}

// Crear nueva transacción
export async function crearTransaccion(data) {
  const res = await fetch(`${API_URL}/transacciones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Error creando transacción");
  }

  return res.json();
}

// Eliminar transacción
export async function eliminarTransaccion(id) {
  const res = await fetch(`${API_URL}/transacciones/${id}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Error eliminando transacción");
  }

  return res.json();
}

// Modificar transacción
export async function modificarTransaccion(id, data) {
  const res = await fetch(`${API_URL}/transacciones/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Error modificando transacción");
  }

  return res.json();
}

// Obtener balance
export async function obtenerBalance() {
  const res = await fetch(`${API_URL}/balance`);
  if (!res.ok) throw new Error("Error obteniendo balance");
  return res.json();
}
