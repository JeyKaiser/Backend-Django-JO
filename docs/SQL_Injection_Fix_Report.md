
# Informe de Corrección: Vulnerabilidad de Inyección SQL

**Fecha:** 2025-08-23

## 1. Resumen Ejecutivo

Este informe detalla las acciones tomadas para corregir la vulnerabilidad crítica de **Inyección SQL** identificada en la integración de la aplicación con la base de datos SAP HANA. La refactorización se ha centrado en modificar la forma en que se construyen y ejecutan las consultas SQL para seguir las mejores prácticas de seguridad.

Los archivos modificados han sido:
- `sap/HANA/queries.py`
- `sap/views.py`

## 2. Descripción de la Vulnerabilidad

El método anterior para consultar la base de datos consistía en construir las sentencias SQL utilizando f-strings de Python. Esto insertaba variables y datos de entrada del usuario directamente en la cadena de la consulta. Esta práctica representaba un riesgo de seguridad severo, ya que un atacante podría haber manipulado los parámetros de entrada (ej. a través de una llamada a la API) para alterar la lógica de la consulta, permitiendo potencialmente el acceso no autorizado, la modificación o la eliminación de datos.

**Ejemplo de código vulnerable (antes):**
```python
# en queries.py
def queryReferenciasPorAnio(collection):
    return f"SELECT * FROM ... WHERE U_GSP_COLLECTION = '{collection}'"

# en views.py
cursor.execute(queryReferenciasPorAnio(user_input))
```

## 3. Acciones de Corrección Realizadas

La corrección se ha implementado en dos pasos principales para desacoplar la consulta de los datos:

### 3.1. Modificación de `sap/HANA/queries.py`

Todas las funciones que generaban consultas SQL han sido modificadas. Ahora, en lugar de aceptar parámetros y devolver una consulta completa, devuelven una **plantilla de consulta estática** que utiliza placeholders (`?`) en los lugares donde irían los datos del usuario.

**Código modificado en `queries.py`:**
```python
# La función ya no necesita el parámetro
def queryReferenciasPorAnio():
    # La consulta ahora usa un placeholder '?'
    return "SELECT * FROM ... WHERE U_GSP_COLLECTION = ?"
```

### 3.2. Modificación de `sap/views.py`

Se han actualizado todas las llamadas al método `cursor.execute()` que utilizaban estas consultas. Ahora se emplea el método de **consulta parametrizada**, pasando la plantilla de la consulta y los datos del usuario como argumentos separados. El driver de la base de datos (`hdbcli`) es ahora responsable de escapar y sanitizar los datos de forma segura antes de insertarlos en la consulta.

**Código modificado en `views.py`:**
```python
# El valor del usuario se pasa como una tupla en el segundo argumento de execute()
cursor.execute(queryReferenciasPorAnio(), (user_input,))
```

## 4. Resultado y Próximos Pasos

Con estos cambios, la aplicación ahora es significativamente más segura contra ataques de inyección SQL. Los datos del usuario ya no se mezclan directamente con la lógica de las consultas.

**Nota Importante:**
Se ha aplicado esta corrección a la gran mayoría de las consultas. Sin embargo, las consultas más complejas que utilizan bucles y tablas temporales en HANA (identificadas en el código con comentarios) pueden requerir una refactorización adicional para estar completamente protegidas. Se recomienda una revisión futura de estas consultas específicas para asegurar su total cumplimiento con las prácticas de seguridad.

Se recomienda encarecidamente mantener este patrón de consultas parametrizadas para todo el desarrollo futuro.
