# API Endpoints para Testing con Postman

## Backend Django - Endpoints Disponibles

### Base URL
```
http://localhost:8000
```

## 1. 🔥 NUEVO - API de Consumos

### Endpoint Principal
- **URL:** `GET /api/consumos/`
- **Descripción:** Consulta consumos de telas por código de referencia PT
- **Parámetro requerido:** `reference` (query parameter)

### Ejemplos de Uso

#### ✅ Consulta Exitosa
```http
GET http://localhost:8000/api/consumos/?reference=PT03708
```

**Respuesta Esperada:**
```json
{
    "success": true,
    "data": [
        {
            "COLECCION": "WINTER SUN 2024",
            "NOMBRE_REF": "PANTALON CASUAL",
            "USO_EN_PRENDA": "PRINCIPAL",
            "COD_TELA": "TEL002",
            "NOMBRE_TELA": "DENIM STRETCH",
            "CONSUMO": 2.80,
            "GRUPO_TALLAS": "STD",
            "LINEA": "CASUAL",
            "tipo": "TELAS"
        }
    ],
    "count": 1,
    "referenceCode": "PT03708"
}
```

#### ❌ Error - Parámetro Faltante
```http
GET http://localhost:8000/api/consumos/
```

**Respuesta:**
```json
{
    "success": false,
    "error": "El parámetro reference es requerido"
}
```

#### ❌ Error - Formato Inválido
```http
GET http://localhost:8000/api/consumos/?reference=ABC123
```

**Respuesta:**
```json
{
    "success": false,
    "error": "El código de referencia debe tener formato PT seguido de números",
    "referenceCode": "ABC123"
}
```

#### 📭 Sin Resultados
```http
GET http://localhost:8000/api/consumos/?reference=PT99999
```

**Respuesta:**
```json
{
    "success": true,
    "data": [],
    "count": 0,
    "referenceCode": "PT99999"
}
```

---

## 2. APIs de Colecciones (Existentes)

### Lista de Colecciones
```http
GET http://localhost:8000/api/colecciones/
```

### Años por Colección
```http
GET http://localhost:8000/api/colecciones/winter-sun/anios/
```

### Referencias por Año
```http
GET http://localhost:8000/api/referencias-por-anio/105/
```

### Detalle de Referencia
```http
GET http://localhost:8000/api/detalle-referencia/PT03522/?collectionId=106
```

### Fases de Referencia
```http
GET http://localhost:8000/api/fases/106/PT03522/md-creacion-ficha/
```

---

## 3. APIs de Búsqueda (Existentes)

### Búsqueda PT Code
```http
GET http://localhost:8000/api/search-pt/?ptCode=PT03708
```

---

## 4. APIs SAP (Módulo SAP)

### Colecciones SAP
```http
GET http://localhost:8000/sap/collections/
```

### Modelos SAP
```http
GET http://localhost:8000/sap/models/
```

---

## 5. APIs de Usuarios

### Lista de Usuarios
```http
GET http://localhost:8000/api/users
```

### Búsqueda de Usuarios
```http
GET http://localhost:8000/api/users/search?q=nombre
```

### Usuario por ID
```http
GET http://localhost:8000/api/users/123
```

### Test Conexión HANA
```http
GET http://localhost:8000/api/test-hana/
```

---

## 6. Autenticación JWT

### Obtener Token
```http
POST http://localhost:8000/api/token/
Content-Type: application/json

{
    "username": "tu_usuario",
    "password": "tu_password"
}
```

### Refrescar Token
```http
POST http://localhost:8000/api/token/refresh/
Content-Type: application/json

{
    "refresh": "tu_refresh_token"
}
```

### Verificar Token
```http
POST http://localhost:8000/api/token/verify/
Content-Type: application/json

{
    "token": "tu_access_token"
}
```

---

## Testing Recomendado

### 1. Consumos API - Casos de Prueba
```bash
# Caso 1: Referencia válida conocida
GET /api/consumos/?reference=PT03708

# Caso 2: Referencia inexistente
GET /api/consumos/?reference=PT99999

# Caso 3: Sin parámetro
GET /api/consumos/

# Caso 4: Formato inválido
GET /api/consumos/?reference=ABC123

# Caso 5: Parámetro vacío
GET /api/consumos/?reference=
```

---

## URLs Principales para Postman

### 🔥 Endpoint Principal de Consumos
- **GET** `http://localhost:8000/api/consumos/?reference=PT03708`

### APIs Core del Sistema
- **GET** `http://localhost:8000/api/colecciones/`
- **GET** `http://localhost:8000/api/search-pt/?ptCode=PT03708`
- **GET** `http://localhost:8000/api/referencias-por-anio/105/`

### Testing de Conexión
- **GET** `http://localhost:8000/api/test-hana/`

La API de consumos está completamente funcional y sincronizada con el frontend Next.js.