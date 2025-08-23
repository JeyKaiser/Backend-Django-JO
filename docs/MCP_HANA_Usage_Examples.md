# Guía de Uso del Servidor MCP HANA

## 📋 **Configuración Necesaria**

### 1. Variables de Entorno
Asegúrate de que estas variables estén definidas en tu `.env`:

```env
HANA_HOST=10.238.117.7
HANA_PORT=30015
HANA_USER=DISENO
HANA_PASSWORD=Diseno2028#
HANA_DATABASE=DISENO
HANA_SCHEMA=GARMENT_PRODUCTION_CONTROL
```

### 2. Configuración MCP
En tu archivo `.claude.json` o configuración MCP:

```json
{
  "mcpServers": {
    "hana-mcp-server": {
      "command": "node",
      "args": ["hana-mcp-server.ts"],
      "env": {
        "HANA_HOST": "10.238.117.7",
        "HANA_PORT": "30015",
        "HANA_USER": "DISENO",
        "HANA_PASSWORD": "Diseno2028#",
        "HANA_DATABASE": "DISENO",
        "HANA_SCHEMA": "GARMENT_PRODUCTION_CONTROL"
      }
    }
  }
}
```

## 🔧 **Herramientas Disponibles en el MCP**

### 1. `query_hana` - Consulta SQL Personalizada

**Estructura:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT * FROM tabla WHERE condicion = ?",
    "schema": "ESQUEMA_OPCIONAL"
  }
}
```

**Ejemplos:**

#### A) Listar todos los esquemas
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT SCHEMA_NAME, SCHEMA_OWNER, CREATE_TIME FROM SYS.SCHEMAS WHERE SCHEMA_NAME NOT LIKE '_SYS_%' ORDER BY SCHEMA_NAME"
  }
}
```

#### B) Ver tablas en un esquema específico
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT TABLE_NAME, TABLE_TYPE FROM SYS.TABLES WHERE SCHEMA_NAME = 'SBOJOZF' ORDER BY TABLE_NAME"
  }
}
```

#### C) Consultar colecciones
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT \"Code\", \"Name\", \"U_GSP_SEASON\" FROM \"@GSP_TCCOLLECTION\" ORDER BY \"U_GSP_SEASON\" DESC",
    "schema": "SBOJOZF"
  }
}
```

### 2. `get_collections` - Obtener Colecciones

**Estructura:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "get_collections",
  "arguments": {
    "filter": "OPCIONAL - filtro de búsqueda"
  }
}
```

**Ejemplo:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "get_collections",
  "arguments": {}
}
```

### 3. `get_references_by_collection` - Referencias por Colección

**Estructura:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "get_references_by_collection",
  "arguments": {
    "collection_id": "063"
  }
}
```

**Ejemplo:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "get_references_by_collection",
  "arguments": {
    "collection_id": "085"
  }
}
```

### 4. `get_fabrics_by_reference` - Telas por Referencia

**Estructura:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "get_fabrics_by_reference",
  "arguments": {
    "reference_id": "PT001",
    "collection_id": "063"
  }
}
```

### 5. `get_materials_by_reference` - Insumos por Referencia

**Estructura:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "get_materials_by_reference",
  "arguments": {
    "reference_id": "PT001",
    "collection_id": "063"
  }
}
```

### 6. `search_pt_code` - Buscar Código PT

**Estructura:**
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "search_pt_code",
  "arguments": {
    "pt_code": "PT001"
  }
}
```

## 📊 **Ejemplos Avanzados de Consultas**

### 1. Análisis de Productos por Colección
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT c.\"Name\" as COLECCION, m.\"U_GSP_REFERENCE\" as REFERENCIA, m.\"U_GSP_Desc\" as DESCRIPCION FROM SBOJOZF.\"@GSP_TCCOLLECTION\" c INNER JOIN SBOJOZF.\"@GSP_TCMODEL\" m ON c.\"Code\" = m.\"U_GSP_COLLECTION\" WHERE c.\"U_GSP_SEASON\" = '2025' ORDER BY c.\"Name\", m.\"U_GSP_REFERENCE\""
  }
}
```

### 2. Consumos de Materiales
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT T1.\"U_GSP_REFERENCE\" as REFERENCIA, T2.\"U_GSP_ItemName\" as MATERIAL, T2.\"U_GSP_QuantMsr\" as CONSUMO FROM SBOJOZF.\"@GSP_TCMODEL\" T1 INNER JOIN SBOJOZF.\"@GSP_TCMODELMAT\" T2 ON T1.\"Code\" = T2.\"U_GSP_ModelCode\" WHERE T1.\"U_GSP_REFERENCE\" = 'PT001'"
  }
}
```

### 3. Inventario de Items
```json
{
  "server_name": "hana-mcp-server",
  "tool_name": "query_hana",
  "arguments": {
    "query": "SELECT \"ItemCode\", \"ItemName\", \"OnHand\", \"InvntryUom\" FROM SBOJOZF.\"OITM\" WHERE \"OnHand\" > 0 ORDER BY \"ItemName\"",
    "schema": "SBOJOZF"
  }
}
```

## 🚀 **Cómo Usar en Claude Code**

Para usar estas consultas en Claude Code, usa el comando:

```
use_mcp_tool con el servidor hana-mcp-server y la herramienta [nombre_herramienta]
```

**Ejemplo completo:**
```
Por favor usa el MCP para mostrarme todas las colecciones disponibles
```

Claude Code ejecutará automáticamente:
```json
{
  "server_name": "hana-mcp-server", 
  "tool_name": "get_collections",
  "arguments": {}
}
```

## ⚠️ **Notas Importantes**

1. **Esquemas**: SAP HANA usa esquemas con nombres sensibles a mayúsculas
2. **Tablas**: Las tablas personalizadas empiezan con `@` (ej: `@GSP_TCCOLLECTION`)
3. **Campos**: Los campos se encierran en comillas dobles (ej: `"U_GSP_REFERENCE"`)
4. **Parámetros**: Usa parámetros SQL seguros, nunca concatenes strings directamente

## 🔧 **Solución de Problemas**

Si el MCP no funciona:

1. Verifica las variables de entorno con: `echo $HANA_HOST`
2. Ejecuta el script de diagnóstico: `python test_hana_connection.py`
3. Revisa los logs del servidor MCP en la terminal
4. Usa las APIs Django directas como fallback desde `sap/views.py`