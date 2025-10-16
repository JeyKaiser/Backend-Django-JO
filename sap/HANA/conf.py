
from hdbcli import dbapi
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_hana_connection(schema_name='SBOJOZF'):
    """
    Establece una nueva conexión a la base de datos SAP HANA.
    Esta función debe ser llamada para cada petición que requiera una conexión a la BD.
    Asegura que cada petición tenga su propia conexión aislada.

    Args:
        schema_name (str, optional): El nombre del esquema a usar. Defaults to 'SBOJOZF'.

    Returns:
        dbapi.Connection: Un objeto de conexión de hdbcli, o None si la conexión falla.
    """
    try:
        # Accede a la configuración de HANA desde el settings de Django
        hana_config = settings.HANA_CONFIG
        
        conn = dbapi.connect(
            address=hana_config['address'],
            port=hana_config['port'],
            user=hana_config['user'],
            password=hana_config['password'],
            currentschema=schema_name,
            encrypt=hana_config.get('encrypt', True), # Usar .get para valores opcionales
            sslValidateCertificate=hana_config.get('sslValidateCertificate', False)
        )
        logger.info(f"Nueva conexión a HANA establecida para el esquema: {schema_name}")
        return conn
    except Exception as e:
        logger.critical(f"FALLO CRÍTICO AL CONECTAR CON SAP HANA para el esquema {schema_name}: {e}", exc_info=True)
        return None
