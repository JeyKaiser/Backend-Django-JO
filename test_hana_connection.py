#!/usr/bin/env python3

"""
Script de diagnóstico para probar la conexión a SAP HANA
y mostrar esquemas disponibles
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
sys.path.append(str(Path(__file__).resolve().parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JO_System_Project.settings')

import django
django.setup()

from django.conf import settings
import logging
from hdbcli import dbapi

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_hana_connection():
    """Prueba la conexión básica a SAP HANA"""
    logger.info("=== DIAGNÓSTICO DE CONEXIÓN SAP HANA ===")
    
    # Mostrar configuración
    hana_config = settings.HANA_CONFIG
    logger.info(f"Host: {hana_config['address']}")
    logger.info(f"Puerto: {hana_config['port']}")
    logger.info(f"Usuario: {hana_config['user']}")
    logger.info(f"Base de datos: {hana_config['database']}")
    logger.info(f"Esquema por defecto: {hana_config['schema']}")
    
    try:
        # Intentar conexión básica
        logger.info("Intentando conectar a SAP HANA...")
        conn = dbapi.connect(
            address=hana_config['address'],
            port=hana_config['port'],
            user=hana_config['user'],
            password=hana_config['password'],
            encrypt=hana_config.get('encrypt', True),
            sslValidateCertificate=hana_config.get('sslValidateCertificate', False)
        )
        
        logger.info("✅ Conexión exitosa a SAP HANA")
        
        # Obtener información de la base de datos
        cursor = conn.cursor()
        
        # Consultar versión de HANA
        cursor.execute("SELECT VERSION FROM SYS.M_DATABASE")
        version = cursor.fetchone()
        logger.info(f"Versión HANA: {version[0] if version else 'No disponible'}")
        
        # Consultar esquemas disponibles
        logger.info("\n=== ESQUEMAS DISPONIBLES ===")
        cursor.execute("""
            SELECT SCHEMA_NAME, SCHEMA_OWNER, CREATE_TIME 
            FROM SYS.SCHEMAS 
            WHERE SCHEMA_NAME NOT LIKE '_SYS_%' 
            ORDER BY SCHEMA_NAME
        """)
        
        esquemas = cursor.fetchall()
        if esquemas:
            for esquema in esquemas:
                logger.info(f"- {esquema[0]} (Owner: {esquema[1]}, Created: {esquema[2]})")
        else:
            logger.warning("No se encontraron esquemas disponibles")
            
        # Verificar si el esquema por defecto existe
        cursor.execute(
            "SELECT COUNT(*) FROM SYS.SCHEMAS WHERE SCHEMA_NAME = ?",
            (hana_config['schema'],)
        )
        schema_exists = cursor.fetchone()[0]
        
        if schema_exists:
            logger.info(f"✅ Esquema '{hana_config['schema']}' existe")
            
            # Listar tablas en el esquema por defecto
            cursor.execute(f"""
                SELECT TABLE_NAME, TABLE_TYPE 
                FROM SYS.TABLES 
                WHERE SCHEMA_NAME = '{hana_config['schema']}'
                ORDER BY TABLE_NAME
            """)
            
            tablas = cursor.fetchall()
            logger.info(f"\n=== TABLAS EN ESQUEMA '{hana_config['schema']}' ===")
            if tablas:
                for tabla in tablas[:10]:  # Mostrar solo las primeras 10
                    logger.info(f"- {tabla[0]} ({tabla[1]})")
                if len(tablas) > 10:
                    logger.info(f"... y {len(tablas) - 10} tablas más")
            else:
                logger.warning(f"No se encontraron tablas en el esquema '{hana_config['schema']}'")
                
        else:
            logger.error(f"❌ Esquema '{hana_config['schema']}' NO existe")
            
        # Verificar esquema SBOJOZF (usado en las consultas)
        cursor.execute(
            "SELECT COUNT(*) FROM SYS.SCHEMAS WHERE SCHEMA_NAME = 'SBOJOZF'"
        )
        sbojozf_exists = cursor.fetchone()[0]
        
        if sbojozf_exists:
            logger.info("✅ Esquema 'SBOJOZF' existe")
            
            # Listar algunas tablas importantes
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM SYS.TABLES 
                WHERE SCHEMA_NAME = 'SBOJOZF' 
                AND TABLE_NAME IN ('@GSP_TCCOLLECTION', '@GSP_TCMODEL', 'OITM')
                ORDER BY TABLE_NAME
            """)
            
            tablas_importantes = cursor.fetchall()
            logger.info("Tablas importantes encontradas:")
            for tabla in tablas_importantes:
                logger.info(f"- SBOJOZF.{tabla[0]}")
        else:
            logger.warning("⚠️ Esquema 'SBOJOZF' NO existe")
        
        cursor.close()
        conn.close()
        logger.info("✅ Conexión cerrada correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error de conexión a SAP HANA: {str(e)}")
        logger.error(f"Tipo de error: {type(e).__name__}")
        return False
    
    return True

def test_mcp_server_config():
    """Prueba la configuración del servidor MCP"""
    logger.info("\n=== DIAGNÓSTICO SERVIDOR MCP HANA ===")
    
    # Verificar variables de entorno para MCP
    mcp_vars = [
        'HANA_HOST', 'HANA_PORT', 'HANA_USER', 
        'HANA_PASSWORD', 'HANA_DATABASE', 'HANA_SCHEMA'
    ]
    
    for var in mcp_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✅ {var}: {value[:5]}{'*' * (len(value) - 5) if len(value) > 5 else value}")
        else:
            logger.error(f"❌ {var}: NO DEFINIDA")

if __name__ == "__main__":
    print("Iniciando diagnóstico de SAP HANA...")
    
    # Probar configuración MCP
    test_mcp_server_config()
    
    # Probar conexión HANA
    success = test_hana_connection()
    
    if success:
        print("\n✅ Diagnóstico completado exitosamente")
    else:
        print("\n❌ Se encontraron errores durante el diagnóstico")