// src/Layout.jsx
import { Link, Outlet } from "react-router-dom";
import "./layout.css";

export default function Layout() {
  return (
    <div className="layout">
      
      {/* SIDEBAR */}
      <aside className="sidebar">
        <h2 className="sidebar-title">Menú</h2>

        <nav className="sidebar-links">
          <Link to="/">Historial de transacciones</Link>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/resumen">Resumen del mes</Link>
          <Link to="/eliminar">Eliminar transacción</Link>
          <Link to="/todas">Todas</Link>
        </nav>
      </aside>

      {/* CONTENIDO PRINCIPAL */}
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
