# 🔧 PROMPT PARA CLAUDE CODE - FRONTEND NEXT.JS

## PROBLEMA IDENTIFICADO

El módulo de consumos del frontend Next.js está consultando datos incorrectos debido a configuración de URL errónea. Está consultando `localhost:3000/api/consumos` (endpoint mock de Next.js) en lugar de `localhost:8000/api/consumos` (API real de Django).

## EVIDENCIA DEL PROBLEMA

**Frontend actual devuelve datos mock:**
```json
{
  "COLECCION": "WINTER SUN",
  "NOMBRE_REF": "PANTALON CASUAL WINTER", 
  "USO_EN_PRENDA": "FORRO",
  "COD_TELA": "TEL002",
  "NOMBRE_TELA": "DENIM STRETCH",
  "CONSUMO": 2.80
}
```

**API Django real devuelve (verificado en Postman):**
```json
{
  "COLECCION": "SPRING SUMMER 2026",
  "NOMBRE REF": "ECRU MANLY BLUES SHIRT",
  "USO EN PRENDA": "TELA DE LUCIR", 
  "COD TELA": "TE00000027",
  "NOMBRE TELA": "COTTON POPLIN ACTION TC4778/R1 ECRU COL.14909",
  "CONSUMO": 2.01
}
```

## TAREAS A REALIZAR

### 1. IDENTIFICAR EL CÓDIGO PROBLEMÁTICO
Buscar en el código del frontend Next.js la línea que contiene:
```javascript
const response = await fetch(`/api/consumos?reference=${encodeURIComponent(searchCode.trim())}`, {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 2. CAMBIAR LA URL A LA API REAL DE DJANGO
Cambiar la URL relativa `/api/consumos` por la URL absoluta del backend Django:

**CAMBIO REQUERIDO:**
```javascript
// ❌ ACTUAL (incorrecto)
const response = await fetch(`/api/consumos?reference=${encodeURIComponent(searchCode.trim())}`, {

// ✅ NUEVO (correcto)  
const response = await fetch(`http://localhost:8000/api/consumos?reference=${encodeURIComponent(searchCode.trim())}`, {
```

### 3. VERIFICAR Y ELIMINAR ENDPOINT MOCK
- Buscar y eliminar cualquier archivo `/api/consumos/route.js` o similar en la carpeta `app/api/` o `pages/api/`
- Este endpoint mock está devolviendo datos hardcodeados que interfieren con la funcionalidad real

### 4. CONFIGURAR VARIABLE DE ENTORNO (OPCIONAL - RECOMENDADO)
Para mejor mantenimiento, crear una variable de entorno para la URL del backend:

**En `.env.local`:**
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

**En el código:**
```javascript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
const response = await fetch(`${BACKEND_URL}/api/consumos?reference=${encodeURIComponent(searchCode.trim())}`, {
```

### 5. VERIFICAR ESTRUCTURA DE DATOS
Asegurarse de que el frontend maneje correctamente la estructura de respuesta de Django:
```json
{
  "success": true,
  "data": [...],
  "count": 2,
  "referenceCode": "PT03708"
}
```

### 6. TESTING
- Probar con códigos PT03708, PT03710, PT03412
- Verificar que los datos mostrados coincidan con los de Postman
- Confirmar que se muestran los datos reales de SAP HANA, no datos mock

## ESTRUCTURA ESPERADA DE RESPUESTA DJANGO

```typescript
interface ConsumosResponse {
  success: boolean;
  data: Array<{
    COLECCION: string;
    "NOMBRE REF": string;  // ⚠️ NOTA: Contiene ESPACIOS, no guiones bajos
    "USO EN PRENDA": string;
    "COD TELA": string; 
    "NOMBRE TELA": string;
    CONSUMO: number;
    "GRUPO TALLAS": string;
    LINEA: string;
    tipo: string;
  }>;
  count: number;
  referenceCode: string;
}
```

## ENDPOINT DE DJANGO CONFIRMADO FUNCIONAL

✅ **URL:** `GET http://localhost:8000/api/consumos?reference={codigo_pt}`
✅ **Validado con:** PT03708, PT03710, PT03412  
✅ **Status:** Completamente funcional y conectado a SAP HANA
✅ **Documentación:** Backend incluye logging detallado para debugging

## NOTAS IMPORTANTES

- El backend Django está **100% funcional** - no requiere cambios
- El problema es únicamente de configuración de URL en frontend
- Los datos mock del frontend tienen estructura diferente (`NOMBRE_REF` vs `NOMBRE REF`)
- Una vez aplicados los cambios, el frontend mostrará datos reales de la base de datos SAP HANA

---

**PRIORIDAD:** Alta - Los usuarios ven datos incorrectos  
**COMPLEJIDAD:** Baja - Cambio de URL simple  
**TIEMPO ESTIMADO:** 15-30 minutos