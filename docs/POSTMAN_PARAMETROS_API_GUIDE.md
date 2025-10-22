# Guía de Pruebas API - Parámetros con Postman

## Configuración Base
- **URL Base**: `http://localhost:8000`
- **Headers requeridos**: `Content-Type: application/json`

---

## 1. Obtener Opciones para Formularios (GET)

### Base Textil
```
GET http://localhost:8000/api/sap/base_textil/
```

### Tela
```
GET http://localhost:8000/api/sap/tela/
```

### Print
```
GET http://localhost:8000/api/sap/print/
```

### Hilo de Tela
```
GET http://localhost:8000/api/sap/hilo_tela/
```

### Hilo de Molde
```
GET http://localhost:8000/api/sap/hilo_molde/
```

### Canal Tela
```
GET http://localhost:8000/api/sap/canal_tela/
```

### Sentido Sesgos
```
GET http://localhost:8000/api/sap/sentido_sesgos/
```

### Rotación Molde
```
GET http://localhost:8000/api/sap/rotacion_molde/
```

### Restricciones Tela
```
GET http://localhost:8000/api/sap/restricciones_tela/
```

---

## 2. Crear Parámetro (POST)

### Endpoint
```
POST http://localhost:8000/api/sap/parametros/
```

### Headers
```
Content-Type: application/json
```

### Body (JSON) - Ejemplo 1
```json
{
    "CODIGO": "001",
    "BASE_TEXTIL_ID": 8,
    "TELA_ID": 1,
    "PRINT_ID": 1,
    "HILO_DE_TELA_ID": 2,
    "HILO_DE_MOLDE_ID": 2,
    "CANAL_TELA_ID": 1,
    "SENTIDO_SESGOS_ID": 2,
    "ROTACION_MOLDE_ID": 2,
    "RESTRICCIONES_ID": 7
}
```

### Body (JSON) - Ejemplo 2
```json
{
    "CODIGO": "002",
    "BASE_TEXTIL_ID": 5,
    "TELA_ID": 3,
    "PRINT_ID": 2,
    "HILO_DE_TELA_ID": 1,
    "HILO_DE_MOLDE_ID": 3,
    "CANAL_TELA_ID": 2,
    "SENTIDO_SESGOS_ID": 1,
    "ROTACION_MOLDE_ID": 1,
    "RESTRICCIONES_ID": 3
}
```

### Body (JSON) - Ejemplo 3
```json
{
    "CODIGO": "003",
    "BASE_TEXTIL_ID": 1,
    "TELA_ID": 2,
    "PRINT_ID": 3,
    "HILO_DE_TELA_ID": 3,
    "HILO_DE_MOLDE_ID": 1,
    "CANAL_TELA_ID": 3,
    "SENTIDO_SESGOS_ID": 3,
    "ROTACION_MOLDE_ID": 3,
    "RESTRICCIONES_ID": 1
}
```

---

## 3. Respuestas Esperadas

### Éxito (201 Created)
```json
{
    "success": "Parámetro creado exitosamente con ID: 1"
}
```

### Error - Campo Faltante (400 Bad Request)
```json
{
    "error": "El campo 'CODIGO' es obligatorio."
}
```

### Error - ID No Existe (400 Bad Request)
```json
{
    "error": "El ID '999' no existe en la tabla 'BASE_TEXTIL'."
}
```

### Error - Servidor (500 Internal Server Error)
```json
{
    "error": "Error al insertar el registro en la base de datos."
}
```

---

## 4. Listar Parámetros Creados (GET)

### Endpoint
```
GET http://localhost:8000/api/sap/parametros/
```

### Respuesta Esperada
```json
[
    {
        "ID": 1,
        "CODIGO": "001",
        "BASE_TEXTIL_ID": 8,
        "TELA_ID": 1,
        "PRINT_ID": 1,
        "HILO_DE_TELA_ID": 2,
        "HILO_DE_MOLDE_ID": 2,
        "CANAL_TELA_ID": 1,
        "SENTIDO_SESGOS_ID": 2,
        "ROTACION_MOLDE_ID": 2,
        "RESTRICCIONES_ID": 7
    }
]
```

---

## 5. Colección de Postman (Importar en Postman)

```json
{
    "info": {
        "name": "SAP Parámetros API",
        "description": "Colección para probar endpoints de parámetros SAP HANA",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Obtener BASE_TEXTIL",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://localhost:8000/api/sap/base_textil/",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["api", "sap", "base_textil", ""]
                }
            }
        },
        {
            "name": "Obtener TELA",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://localhost:8000/api/sap/tela/",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["api", "sap", "tela", ""]
                }
            }
        },
        {
            "name": "Crear Parámetro",
            "request": {
                "method": "POST",
                "header": [
                    {
                        "key": "Content-Type",
                        "value": "application/json"
                    }
                ],
                "body": {
                    "mode": "raw",
                    "raw": "{\n    \"CODIGO\": \"001\",\n    \"BASE_TEXTIL_ID\": 8,\n    \"TELA_ID\": 1,\n    \"PRINT_ID\": 1,\n    \"HILO_DE_TELA_ID\": 2,\n    \"HILO_DE_MOLDE_ID\": 2,\n    \"CANAL_TELA_ID\": 1,\n    \"SENTIDO_SESGOS_ID\": 2,\n    \"ROTACION_MOLDE_ID\": 2,\n    \"RESTRICCIONES_ID\": 7\n}"
                },
                "url": {
                    "raw": "http://localhost:8000/api/sap/parametros/",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["api", "sap", "parametros", ""]
                }
            }
        },
        {
            "name": "Listar Parámetros",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "http://localhost:8000/api/sap/parametros/",
                    "protocol": "http",
                    "host": ["localhost"],
                    "port": "8000",
                    "path": ["api", "sap", "parametros", ""]
                }
            }
        }
    ]
}
```

---

## 6. Pasos para Probar en Postman

1. **Abrir Postman**
2. **Importar la colección** (usar el JSON de arriba)
3. **Verificar que Django esté corriendo**: `python manage.py runserver`
4. **Primero obtener las opciones disponibles** ejecutando los GET de cada tabla
5. **Usar los IDs obtenidos** para crear el payload del POST
6. **Ejecutar el POST** para crear el parámetro
7. **Verificar con GET** que el parámetro se creó correctamente

## 7. Ejemplos de IDs Válidos
(Ejecutar primero los endpoints GET para obtener IDs reales de tu base de datos)

```
BASE_TEXTIL_ID: 1, 2, 3, 8...
TELA_ID: 1, 2, 3...
PRINT_ID: 1, 2, 3...
HILO_DE_TELA_ID: 1, 2, 3...
(etc.)
```

**¡Importante!** Los IDs deben existir en las tablas correspondientes o recibirás un error 400.