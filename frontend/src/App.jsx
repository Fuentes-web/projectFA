import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import ResumenMensual from "./pages/ResumenMensual";
import Layout from "./Layout";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/resumen" element={<ResumenMensual />} />

          {/* rutas nuevas del sidebar */}
          <Route path="/eliminar" element={<div><h2>Eliminar transacción</h2></div>} />
          <Route path="/todas" element={<div><h2>Todas las transacciones</h2></div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
