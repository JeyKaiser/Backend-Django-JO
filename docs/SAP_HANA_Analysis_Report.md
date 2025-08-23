
# Análisis Definitivo de la Integración con SAP HANA

He examinado los archivos `sap/views.py`, `sap/HANA/conf.py` y `sap/HANA/queries.py`. A continuación, se detalla el flujo completo y los hallazgos.

## ¿Cómo y Cuándo se Consulta a SAP HANA?

1.  **Disparador (Cuándo):** La consulta se inicia cuando un cliente (ej. el frontend en Next.js) hace una petición a un endpoint de la API definido en `sap/views.py`. Por ejemplo, al solicitar los consumos de una referencia.

2.  **Conexión (Cómo - Parte 1):** El archivo `sap/HANA/conf.py` crea un **objeto de conexión global y compartido** (`conn`) en el momento en que se inicia el servidor de Django. Este mismo objeto se reutiliza para todas las peticiones, lo cual es una **práctica peligrosa y no escalable** que puede causar corrupción de datos y fallos bajo carga.

3.  **Lógica de la Vista (Cómo - Parte 2):** Una función o vista en `sap/views.py` se encarga de la petición. Esta importa la conexión `conn` y las funciones de consulta (ej. `queryConsumosPorReferencia`) desde los otros archivos.

4.  **Construcción de la Consulta (Cómo - Parte 3):** El archivo `sap/HANA/queries.py` contiene docenas de funciones. Cada una de ellas **construye una cadena de texto con la consulta SQL** usando f-strings de Python, insertando los parámetros (ej. el código de la referencia) directamente en la cadena de la consulta.

5.  **Ejecución (Cómo - Parte 4):** La vista usa la conexión `conn` para crear un cursor y ejecuta la cadena de la consulta SQL obtenida del paso anterior. Luego procesa los resultados y los devuelve como una respuesta JSON.

---

## Hallazgos Críticos y Plan de Acción

He identificado dos problemas de alta severidad que requieren tu atención inmediata.

### 1. (CRÍTICO) Vulnerabilidad de Inyección SQL (SQL Injection)

*   **Problema:** La forma en que se construyen las consultas en `sap/HANA/queries.py` es el ejemplo clásico de un riesgo de inyección SQL. Al insertar variables directamente en la cadena de la consulta (`f"WHERE T1.U_GSP_REFERENCE = '{ptCode}'"`), un atacante podría enviar un valor malicioso como `ptCode` que altere la lógica de la consulta, permitiéndole extraer, modificar o eliminar datos a los que no debería tener acceso.
*   **Solución Inmediata:** Debes **parametrizar todas las consultas**. En lugar de usar f-strings para insertar los valores, se deben usar placeholders (`?`) en la consulta, y pasar los valores como una tupla en el método `cursor.execute()`. El driver de la base de datos se encarga de escapar los valores de forma segura.

    **Ejemplo de Código Inseguro (Actual):**
    ```python
    # En queries.py
    def queryReferenciasPorAnio(collection):
        query = f"SELECT ... WHERE U_GSP_COLLECTION = '{collection}'"
        return query

    # En views.py
    cursor.execute(queryReferenciasPorAnio(collection_id))
    ```

    **Ejemplo de Código Seguro (Recomendado):**
    ```python
    # En queries.py
    def queryReferenciasPorAnio():
        # La consulta ahora tiene un placeholder '?'
        query = "SELECT ... WHERE U_GSP_COLLECTION = ?"
        return query

    # En views.py
    # El valor se pasa como un segundo argumento a execute()
    cursor.execute(queryReferenciasPorAnio(), (collection_id,))
    ```

### 2. (CRÍTICO) Conexión de Base de Datos Global y Compartida

*   **Problema:** El objeto `conn` en `sap/HANA/conf.py` es compartido por toda la aplicación. Esto provocará fallos impredecibles y problemas de concurrencia cuando más de un usuario utilice la aplicación simultáneamente.
*   **Solución:** Debes refactorizar el manejo de la conexión para que no sea global. La solución ideal es usar un **pool de conexiones**. Una solución más simple y segura que la actual es encapsular la creación de la conexión en una función que se llame cada vez que se necesite.

    **Ejemplo de Refactorización (Solución simple):**

    **Paso 1: Modificar `sap/HANA/conf.py`**
    Elimina el objeto `conn` global y en su lugar crea una función.

    ```python
    # sap/HANA/conf.py
    from hdbcli import dbapi
    from JO_System_Project.settings import HANA_DB_ADDRESS, HANA_DB_PASS, ...
    import logging

    logger = logging.getLogger(__name__)

    def get_hana_connection():
        """
        Crea y devuelve una nueva conexión a SAP HANA.
        Esta función debe ser llamada cada vez que se necesite una conexión.
        """
        try:
            conn = dbapi.connect(
                address=HANA_DB_ADDRESS,
                port=HANA_DB_PORT,
                user=HANA_DB_USER,
                password=HANA_DB_PASS,
            )
            return conn
        except Exception as e:
            # Es importante registrar el error
            logger.error(f"Error al conectar con SAP HANA: {e}")
            return None
    ```

    **Paso 2: Modificar `sap/views.py`**
    En cada función que usa la base de datos, llama a `get_hana_connection()` para obtener una conexión fresca y asegúrate de cerrarla.

    ```python
    # sap/views.py
    from .HANA.conf import get_hana_connection # Importar la nueva función
    from .HANA.queries import queryReferenciasPorAnio
    import logging

    logger = logging.getLogger(__name__)

    def referenciasPorAnio(collection_id):
        conn = None  # Inicializar conn a None
        cursor = None # Inicializar cursor a None
        try:
            conn = get_hana_connection()
            if conn:
                cursor = conn.cursor()
                # ... (el resto de tu lógica con el cursor)
                # Ejemplo:
                database = 'SBOJOZF'
                cursor.execute(querySelectDataBase(database))
                cursor.execute(queryReferenciasPorAnio(), (collection_id,)) # Usando la consulta parametrizada
                rows = cursor.fetchall()
                # ... procesar datos ...
                return data
        except Exception as e:
            logger.error(f"Error en la vista referenciasPorAnio: {e}")
            # Manejar el error apropiadamente
        finally:
            # Asegurarse de cerrar cursor y conexión
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    ```
