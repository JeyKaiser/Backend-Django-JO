#!/usr/bin/env python3

"""
Script para mostrar las columnas de la tabla OITM en SAP HANA
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

def get_oitm_columns():
    """Obtiene las columnas de la tabla OITM"""
    logger.info("=== COLUMNAS DE LA TABLA OITM EN SAP HANA ===")
    
    hana_config = settings.HANA_CONFIG
    
    try:
        # Conectar a SAP HANA
        conn = dbapi.connect(
            address=hana_config['address'],
            port=hana_config['port'],
            user=hana_config['user'],
            password=hana_config['password'],
            encrypt=hana_config.get('encrypt', True),
            sslValidateCertificate=hana_config.get('sslValidateCertificate', False)
        )
        
        logger.info("✅ Conexión exitosa a SAP HANA")
        cursor = conn.cursor()
        
        # Consulta para obtener las columnas de OITM en el esquema SBOJOZF
        query = """
            SELECT 
                COLUMN_NAME, 
                DATA_TYPE_NAME, 
                LENGTH, 
                SCALE,
                IS_NULLABLE,
                DEFAULT_VALUE,
                COMMENTS
            FROM SYS.TABLE_COLUMNS 
            WHERE SCHEMA_NAME = 'SBOJOZF' 
            AND TABLE_NAME = 'OITM' 
            ORDER BY POSITION
        """
        
        cursor.execute(query)
        columns = cursor.fetchall()
        
        if columns:
            logger.info(f"\n📊 TABLA: SBOJOZF.OITM")
            logger.info(f"📈 Total de columnas: {len(columns)}")
            logger.info("\n" + "="*120)
            logger.info(f"{'COLUMNA':<25} {'TIPO':<20} {'LONGITUD':<10} {'ESCALA':<8} {'NULO':<8} {'COMENTARIO'}")
            logger.info("="*120)
            
            for col in columns:
                column_name = col[0] or ''
                data_type = col[1] or ''
                length = str(col[2]) if col[2] is not None else ''
                scale = str(col[3]) if col[3] is not None else ''
                nullable = 'SÍ' if col[4] == 'TRUE' else 'NO'
                comments = col[6] or ''
                
                # Formatear para mejor visualización
                if length and scale and scale != '0':
                    type_display = f"{data_type}({length},{scale})"
                elif length and data_type in ['NVARCHAR', 'VARCHAR', 'CHAR']:
                    type_display = f"{data_type}({length})"
                else:
                    type_display = data_type
                
                logger.info(f"{column_name:<25} {type_display:<20} {length:<10} {scale:<8} {nullable:<8} {comments}")
            
            logger.info("="*120)
            
            # Mostrar algunas columnas importantes
            logger.info("\n🔑 COLUMNAS IMPORTANTES IDENTIFICADAS:")
            important_columns = [
                'ItemCode', 'ItemName', 'FrgnName', 'ItmsGrpCod', 'CstGrpCode',
                'VatGourpSa', 'CodeBars', 'VATLiable', 'PrchseItem', 'SellItem',
                'InvntItem', 'OnHand', 'IsCommited', 'OnOrder', 'AvgPrice',
                'LastPurPrc', 'LastPurCur', 'LastPurDat', 'ExitCur', 'ExitPrice',
                'ExitWH', 'CreateDate', 'UpdateDate', 'validFor', 'validFrom',
                'validTo', 'frozenFor', 'frozenFrom', 'frozenTo'
            ]
            
            found_important = []
            for col in columns:
                if col[0] in important_columns:
                    found_important.append(col[0])
            
            for imp_col in found_important[:10]:  # Mostrar las primeras 10
                logger.info(f"  ✓ {imp_col}")
                
            if len(found_important) > 10:
                logger.info(f"  ... y {len(found_important) - 10} columnas más")
        
        else:
            logger.warning("❌ No se encontraron columnas para la tabla SBOJOZF.OITM")
            
        # Verificar si existe la tabla
        cursor.execute("""
            SELECT COUNT(*) FROM SYS.TABLES 
            WHERE SCHEMA_NAME = 'SBOJOZF' AND TABLE_NAME = 'OITM'
        """)
        table_exists = cursor.fetchone()[0]
        
        if table_exists == 0:
            logger.error("❌ La tabla SBOJOZF.OITM no existe")
        else:
            logger.info(f"✅ Tabla SBOJOZF.OITM confirmada ({len(columns)} columnas)")
            
        cursor.close()
        conn.close()
        logger.info("✅ Conexión cerrada correctamente")
        
        return columns
        
    except Exception as e:
        logger.error(f"❌ Error consultando columnas de OITM: {str(e)}")
        return None

if __name__ == "__main__":
    print("Consultando columnas de la tabla OITM en SAP HANA...")
    columns = get_oitm_columns()
    
    if columns:
        print(f"\n✅ Consulta completada exitosamente - {len(columns)} columnas encontradas")
    else:
        print("\n❌ Error en la consulta")