# 💰 API de Billetera Personal – FastAPI

Este proyecto es una **API RESTful** desarrollada con **FastAPI** que permite gestionar una **billetera personal virtual**, registrando ingresos, gastos y categorías, así como consultar balances y totales.  
Está pensada como una aplicación base para proyectos de finanzas personales o educación en programación orientada a objetos y desarrollo de APIs modernas.

---

## 🧩 Descripción general

La API permite realizar las siguientes operaciones:
- Registrar **ingresos y gastos** con descripción, monto, tipo y categoría.
- Consultar el **historial de transacciones**.
- Modificar o eliminar transacciones existentes.
- Obtener el **balance actual**, **total de ingresos** y **total de gastos**.

El modelo de dominio se implementa mediante clases en `clases.py` que representan los conceptos centrales:
- `Billetera`: Contiene y gestiona las transacciones.
- `Transaction`: Representa un movimiento (ingreso o gasto).
- `Monto`, `Descripcion`, `Tipo`, `Category`: encapsulan las reglas de negocio.
- Excepciones personalizadas: validan errores comunes como montos negativos o textos muy largos.

---

## ⚙️ Tecnologías utilizadas

- 🐍 **Python 3.10+**
- ⚡ **FastAPI** – Framework para crear APIs rápidas y modernas.
- 🧰 **Pydantic** – Validación de datos.
- 📦 **Uvicorn** – Servidor ASGI para ejecutar la aplicación.
- 🕓 **Datetime / UUID** – Manejo de fechas y claves únicas.

---

## 🏗️ Estructura del proyecto

```
📦 proyecto-billetera
 ┣ 📜 main.py          # Punto de entrada principal (define los endpoints)
 ┣ 📜 clases.py        # Clases, enums y lógica de negocio
 ┣ 📜 requirements.txt # Dependencias del proyecto
 ┗ 📜 README.md        # Documentación principal
```

---

## 🚀 Instalación y ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/proyecto-billetera.git
cd proyecto-billetera
```

### 2️⃣ Crear y activar entorno virtual
```bash
python -m venv venv
venv\Scripts\activate       # En Windows
# o
source venv/bin/activate    # En Linux / Mac
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar el servidor FastAPI
```bash
uvicorn main:app --reload
```

La API estará disponible en:  
👉 **http://127.0.0.1:8000**

Documentación interactiva:  
- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- Redoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧠 Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/transacciones` | Crea una nueva transacción (Ingreso o Gasto). |
| `PUT` | `/transacciones/{id}` | Modifica una transacción existente. |
| `DELETE` | `/transacciones/{id}` | Elimina una transacción. |
| `GET` | `/transacciones` | Lista todas las transacciones registradas. |
| `GET` | `/balance` | Retorna el balance actual, total de ingresos y gastos. |

---

## 📦 Ejemplo de uso

### **POST /transacciones**

**Solicitud**
```json
{
  "descripcion": "Pago de internet",
  "monto": 120.0,
  "tipo": "Gasto",
  "categoria": "Hogar"
}
```

**Respuesta**
```json
{
  "id": "f23d1a76-b22e-4a7a-89a3-66cf18f7d6e8",
  "descripcion": "Pago de internet",
  "monto": 120.0,
  "tipo": "Gasto",
  "categoria": "Hogar",
  "fecha": "2025-10-25T15:30:00.000000"
}
```

---

## ⚠️ Validaciones y excepciones

- `BalanceNegativoException`: evita que un gasto supere el balance disponible.  
- `TextoBreveException`: asegura que la descripción no exceda los 50 caracteres.  
- Validaciones automáticas de **Pydantic** para tipos y valores numéricos.

---

## 🧾 Requerimientos (`requirements.txt`)
