import { useState } from "react";
import Filters from "../components/Filters";
import TransactionList from "../components/TransactionList";
import TransactionForm from "../components/AddTransaccionForm"; // asegúrate de tenerlo

export default function Home() {
  const [filters, setFilters] = useState({});
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-2">Transacciones</h2>

      {/* Botón para abrir formulario */}
      <button 
        className="bg-blue-600 text-white px-4 py-2 rounded mb-4"
        onClick={() => setShowForm(true)}
      >
        Agregar Transacción
      </button>

      <Filters onChange={setFilters} />
      <TransactionList filters={filters} />

      {/* Mostrar formulario si showForm es true */}
      {showForm && (
        <TransactionForm 
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}
