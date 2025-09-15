
import logging
from ..HANA.conf import get_hana_connection

logger = logging.getLogger(__name__)
SCHEMA_NAME = "GARMENT_PRODUCTION_CONTROL"

def _execute_query(query, params=None, fetch=None):
    """
    Ejecutor de consultas genérico para SAP HANA.
    - fetch: puede ser 'all' o 'one'.
    """
    conn = None
    cursor = None
    try:
        conn = get_hana_connection(SCHEMA_NAME)
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos.")
        
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        
        if fetch == 'one':
            result = cursor.fetchone()
            if not result:
                return None
            column_names = [desc[0] for desc in cursor.description]
            return dict(zip(column_names, result))

        if fetch == 'all':
            rows = cursor.fetchall()
            if not rows:
                return []
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]

        # Si no es fetch, es una operación DML (INSERT, UPDATE), confirmamos la transacción.
        conn.commit()
        return True # Éxito en la operación

    except Exception as e:
        logger.error(f"Error en la consulta a HANA: {e}", exc_info=True)
        if conn:
            conn.rollback() # Revertir cambios en caso de error
        return False # Indicar fallo
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_from_table(table_name: str):
    """Obtiene todos los registros de una tabla específica."""
    # ¡IMPORTANTE! Validar table_name para prevenir inyección SQL.
    # Solo permitimos tablas predefinidas.
    allowed_tables = [
        "BASE_TEXTIL", "PRINT", "HILO_DE_TELA", "CANAL_TELA", 
        "ROTACION_MOLDE", "SENTIDO_SESGOS", "RESTRICCIONES_TELA", 
        "HILO_DE_MOLDE", "TELA"
    ]
    if table_name.upper() not in allowed_tables:
        logger.warning(f"Intento de acceso a tabla no permitida: {table_name}")
        return None, "Tabla no válida."

    query = f'SELECT * FROM "{table_name.upper()}";'
    data = _execute_query(query, fetch='all')
    if data is False:
        return None, "Error al consultar la base de datos."
    return data, None

def check_fk_exists(table_name: str, pk_column: str, pk_value: str):
    """Verifica si un ID existe en una tabla."""
    query = f'SELECT COUNT(1) AS "count" FROM "{table_name.upper()}" WHERE "{pk_column.upper()}" = ?;'
    result = _execute_query(query, (pk_value,), fetch='one')
    return result and result['count'] > 0

def create_parametro(data: dict):
    """
    Crea un nuevo registro en la tabla PARAMETROS con validaciones.
    Estructura actualizada según la tabla real de BD.
    """
    required_fields = [
        "CODIGO", "BASE_TEXTIL_ID", "TELA_ID", "PRINT_ID", "HILO_DE_TELA_ID",
        "HILO_DE_MOLDE_ID", "CANAL_TELA_ID", "SENTIDO_SESGOS_ID",
        "ROTACION_MOLDE_ID", "RESTRICCIONES_ID"
    ]
    for field in required_fields:
        if field not in data or data[field] is None:
            return False, f"El campo '{field}' es obligatorio."

    # --- Validaciones de negocio ---
    if len(data["CODIGO"]) > 10:
        return False, "El código no puede superar los 10 caracteres."

    # --- Validación de Claves Foráneas (FK) ---
    fk_checks = {
        "BASE_TEXTIL": ("ID", data["BASE_TEXTIL_ID"]),
        "TELA": ("ID", data["TELA_ID"]),
        "PRINT": ("ID", data["PRINT_ID"]),
        "HILO_DE_TELA": ("ID", data["HILO_DE_TELA_ID"]),
        "HILO_DE_MOLDE": ("ID", data["HILO_DE_MOLDE_ID"]),
        "CANAL_TELA": ("ID", data["CANAL_TELA_ID"]),
        "SENTIDO_SESGOS": ("ID", data["SENTIDO_SESGOS_ID"]),
        "ROTACION_MOLDE": ("ID", data["ROTACION_MOLDE_ID"]),
        "RESTRICCIONES_TELA": ("ID", data["RESTRICCIONES_ID"]),
    }

    for table, (pk_column, pk_value) in fk_checks.items():
        if not check_fk_exists(table, pk_column, pk_value):
            return False, f"El ID '{pk_value}' no existe en la tabla '{table}'."

    # --- Construcción y ejecución de la consulta INSERT ---
    # Generar el próximo ID disponible
    next_id_query = 'SELECT COALESCE(MAX("ID"), 0) + 1 AS "NEXT_ID" FROM "PARAMETROS"'
    next_id_result = _execute_query(next_id_query, fetch='one')
    next_id = next_id_result['NEXT_ID'] if next_id_result else 1

    query = '''
        INSERT INTO "PARAMETROS" (
            "ID", "CODIGO", "BASE_TEXTIL_ID", "TELA_ID", "PRINT_ID", "HILO_DE_TELA_ID",
            "HILO_DE_MOLDE_ID", "CANAL_TELA_ID", "SENTIDO_SESGOS_ID", "ROTACION_MOLDE_ID", "RESTRICCIONES_ID"
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    params = (
        next_id, data["CODIGO"], data["BASE_TEXTIL_ID"], data["TELA_ID"], data["PRINT_ID"],
        data["HILO_DE_TELA_ID"], data["HILO_DE_MOLDE_ID"], data["CANAL_TELA_ID"],
        data["SENTIDO_SESGOS_ID"], data["ROTACION_MOLDE_ID"], data["RESTRICCIONES_ID"]
    )

    success = _execute_query(query, params)

    if not success:
        return False, "Error al insertar el registro en la base de datos."

    return True, f"Parámetro creado exitosamente con ID: {next_id}"
