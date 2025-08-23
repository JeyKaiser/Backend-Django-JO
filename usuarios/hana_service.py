"""
Servicio para conexión directa con SAP HANA usando hdbcli
"""

import hdbcli.dbapi
from django.conf import settings
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class HanaService:
    """Servicio para gestionar conexiones y consultas a SAP HANA"""
    
    def __init__(self):
        self.config = settings.HANA_CONFIG
        self._connection = None
    
    def get_connection(self):
        """Obtiene una conexión a SAP HANA"""
        try:
            if self._connection is None or not self._connection:
                # Configuración básica para SAP HANA
                connection_params = {
                    'address': self.config['address'],
                    'port': int(self.config['port']),
                    'user': self.config['user'],
                    'password': self.config['password'],
                }
                
                # Solo agregar parámetros opcionales si están definidos
                if 'database' in self.config and self.config['database']:
                    connection_params['databaseName'] = self.config['database']
                
                # Configuración de SSL/Encriptación más simple
                if self.config.get('encrypt', False):
                    connection_params['encrypt'] = True
                    connection_params['sslValidateCertificate'] = False
                
                self._connection = hdbcli.dbapi.connect(**connection_params)
                logger.info("Conexión exitosa a SAP HANA")
            return self._connection
        except Exception as e:
            logger.error(f"Error conectando a SAP HANA: {str(e)}")
            raise
    
    def close_connection(self):
        """Cierra la conexión a SAP HANA"""
        if self._connection:
            try:
                self._connection.close()
                self._connection = None
                logger.info("Conexión a SAP HANA cerrada")
            except Exception as e:
                logger.error(f"Error cerrando conexión: {str(e)}")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Ejecuta una consulta SELECT y retorna los resultados
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, params or ())
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        except Exception as e:
            logger.error(f"Error ejecutando consulta: {str(e)}")
            raise
        finally:
            cursor.close()
    
    def execute_non_query(self, query: str, params: tuple = None) -> int:
        """
        Ejecuta una consulta INSERT/UPDATE/DELETE
        Retorna el número de filas afectadas
        """
        connection = self.get_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, params or ())
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            connection.rollback()
            logger.error(f"Error ejecutando operación: {str(e)}")
            raise
        finally:
            cursor.close()


class UsuariosHanaService:
    """Servicio específico para operaciones de usuarios en SAP HANA"""
    
    def __init__(self):
        self.hana = HanaService()
        self.schema = settings.HANA_CONFIG['schema']
        self.table_name = f"{self.schema}.T_USUARIOS"
    
    def get_all_users(self, limit: int = 20, offset: int = 0, filters: Dict = None, search: str = '') -> Dict:
        """Obtiene todos los usuarios con paginación, filtros y búsqueda"""
        
        # Construir condiciones WHERE
        where_conditions = []
        params = []
        
        # Agregar filtros
        if filters:
            if filters.get('area'):
                where_conditions.append("AREA = ?")
                params.append(filters['area'])
            if filters.get('rol'):
                where_conditions.append("ROL = ?")
                params.append(filters['rol'])
            if filters.get('estado'):
                where_conditions.append("ESTADO = ?")
                params.append(filters['estado'])
        
        # Agregar búsqueda
        if search:
            where_conditions.append("(NOMBRE_COMPLETO LIKE ? OR EMAIL LIKE ? OR CODIGO_USUARIO LIKE ?)")
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        # Construir cláusula WHERE
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Consulta para obtener usuarios
        query = f"""
        SELECT * FROM {self.table_name}
        {where_clause}
        ORDER BY FECHA_CREACION DESC
        LIMIT {limit} OFFSET {offset}
        """
        
        # Consulta para obtener el total
        count_query = f"SELECT COUNT(*) as total FROM {self.table_name} {where_clause}"
        
        try:
            users = self.hana.execute_query(query, tuple(params))
            total_result = self.hana.execute_query(count_query, tuple(params))
            total = total_result[0]['TOTAL'] if total_result else 0
            
            return {
                'users': [self._format_user_for_api(user) for user in users],
                'total': total,
                'page': (offset // limit) + 1,
                'limit': limit
            }
        except Exception as e:
            logger.error(f"Error obteniendo usuarios: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Obtiene un usuario por ID"""
        query = f"SELECT * FROM {self.table_name} WHERE ID_USUARIO = ?"
        
        try:
            results = self.hana.execute_query(query, (user_id,))
            if results:
                return self._format_user_for_api(results[0])
            return None
        except Exception as e:
            logger.error(f"Error obteniendo usuario por ID: {str(e)}")
            raise
    
    def get_user_by_code(self, codigo_usuario: str) -> Optional[Dict]:
        """Obtiene un usuario por código"""
        query = f"SELECT * FROM {self.table_name} WHERE CODIGO_USUARIO = ?"
        
        try:
            results = self.hana.execute_query(query, (codigo_usuario,))
            if results:
                return self._format_user_for_api(results[0])
            return None
        except Exception as e:
            logger.error(f"Error obteniendo usuario por código: {str(e)}")
            raise
    
    def create_user(self, user_data: Dict) -> Dict:
        """Crea un nuevo usuario"""
        query = f"""
        INSERT INTO {self.table_name} 
        (CODIGO_USUARIO, NOMBRE_COMPLETO, EMAIL, AREA, ROL, ESTADO, FECHA_CREACION)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        
        params = (
            user_data.get('CODIGO_USUARIO'),
            user_data.get('NOMBRE_COMPLETO'),
            user_data.get('EMAIL'),
            user_data.get('AREA'),
            user_data.get('ROL', 'DISEÑADOR'),
            user_data.get('ESTADO', 'ACTIVO')
        )
        
        try:
            self.hana.execute_non_query(query, params)
            
            # Obtener el usuario creado
            created_user_query = f"SELECT * FROM {self.table_name} WHERE CODIGO_USUARIO = ? ORDER BY FECHA_CREACION DESC LIMIT 1"
            results = self.hana.execute_query(created_user_query, (user_data.get('CODIGO_USUARIO'),))
            
            if results:
                return self._format_user_for_api(results[0])
            raise Exception("No se pudo recuperar el usuario creado")
            
        except Exception as e:
            logger.error(f"Error creando usuario: {str(e)}")
            raise
    
    def update_user(self, user_id: int, user_data: Dict) -> Optional[Dict]:
        """Actualiza un usuario existente"""
        # Construir campos de actualización dinámicamente
        update_fields = []
        params = []
        
        field_mapping = {
            'NOMBRE_COMPLETO': 'NOMBRE_COMPLETO',
            'EMAIL': 'EMAIL',
            'AREA': 'AREA',
            'ROL': 'ROL',
            'ESTADO': 'ESTADO'
        }
        
        for field, column in field_mapping.items():
            if field in user_data and user_data[field] is not None:
                update_fields.append(f"{column} = ?")
                params.append(user_data[field])
        
        if not update_fields:
            # No hay campos para actualizar
            return self.get_user_by_id(user_id)
        
        params.append(user_id)
        
        query = f"""
        UPDATE {self.table_name} 
        SET {', '.join(update_fields)}
        WHERE ID_USUARIO = ?
        """
        
        try:
            affected_rows = self.hana.execute_non_query(query, tuple(params))
            if affected_rows > 0:
                return self.get_user_by_id(user_id)
            return None
        except Exception as e:
            logger.error(f"Error actualizando usuario: {str(e)}")
            raise
    
    def delete_user(self, user_id: int, hard_delete: bool = False) -> bool:
        """Elimina un usuario (soft o hard delete)"""
        if hard_delete:
            # Eliminación permanente
            query = f"DELETE FROM {self.table_name} WHERE ID_USUARIO = ?"
        else:
            # Eliminación suave (cambiar estado a INACTIVO)
            query = f"UPDATE {self.table_name} SET ESTADO = 'INACTIVO' WHERE ID_USUARIO = ?"
        
        try:
            affected_rows = self.hana.execute_non_query(query, (user_id,))
            return affected_rows > 0
        except Exception as e:
            logger.error(f"Error eliminando usuario: {str(e)}")
            raise
    
    def search_users(self, search_term: str, filters: Dict = None, exact_match: bool = False, limit: int = 20) -> List[Dict]:
        """Busca usuarios con filtros avanzados"""
        
        if exact_match:
            # Búsqueda exacta por código de usuario
            base_query = f"""
            SELECT * FROM {self.table_name} 
            WHERE CODIGO_USUARIO = ?
            """
            params = [search_term]
        else:
            # Búsqueda general
            base_query = f"""
            SELECT *, 
                   CASE 
                       WHEN CODIGO_USUARIO LIKE ? THEN 40
                       WHEN NOMBRE_COMPLETO LIKE ? THEN 30
                       WHEN EMAIL LIKE ? THEN 20
                       ELSE 10
                   END as _searchScore
            FROM {self.table_name} 
            WHERE (NOMBRE_COMPLETO LIKE ? OR EMAIL LIKE ? OR CODIGO_USUARIO LIKE ?)
            """
            search_pattern = f"%{search_term}%"
            params = [search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern]
        
        # Agregar filtros adicionales
        if filters:
            if filters.get('area'):
                base_query += " AND AREA = ?"
                params.append(filters['area'])
            if filters.get('rol'):
                base_query += " AND ROL = ?"
                params.append(filters['rol'])
            if filters.get('estado'):
                base_query += " AND ESTADO = ?"
                params.append(filters['estado'])
        
        if exact_match:
            base_query += " ORDER BY FECHA_CREACION DESC"
        else:
            base_query += " ORDER BY _searchScore DESC, FECHA_CREACION DESC"
        
        base_query += f" LIMIT {limit}"
        
        try:
            results = self.hana.execute_query(base_query, tuple(params))
            return [self._format_user_for_api(user) for user in results]
        except Exception as e:
            logger.error(f"Error buscando usuarios: {str(e)}")
            raise
    
    def get_user_options(self) -> Dict:
        """Obtiene opciones para campos del usuario y estadísticas actuales"""
        try:
            # Obtener estadísticas actuales de áreas
            areas_query = f"SELECT AREA, COUNT(*) as USER_COUNT FROM {self.table_name} WHERE ESTADO = 'ACTIVO' GROUP BY AREA"
            current_areas = self.hana.execute_query(areas_query)
            
            # Obtener estadísticas actuales de roles
            roles_query = f"SELECT ROL, COUNT(*) as USER_COUNT FROM {self.table_name} WHERE ESTADO = 'ACTIVO' GROUP BY ROL"
            current_roles = self.hana.execute_query(roles_query)
            
            # Obtener estadísticas de estados
            status_query = f"SELECT ESTADO, COUNT(*) as USER_COUNT FROM {self.table_name} GROUP BY ESTADO"
            status_counts = self.hana.execute_query(status_query)
            
            return {
                'currentAreas': current_areas,
                'currentRoles': current_roles,
                'statusCounts': status_counts
            }
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {str(e)}")
            # Retornar datos vacíos en caso de error
            return {
                'currentAreas': [],
                'currentRoles': [],
                'statusCounts': []
            }
    
    def _format_user_for_api(self, user_data: Dict) -> Dict:
        """Formatea los datos del usuario para la API según especificación"""
        formatted = {
            'ID_USUARIO': user_data.get('ID_USUARIO'),
            'CODIGO_USUARIO': user_data.get('CODIGO_USUARIO', ''),
            'NOMBRE_COMPLETO': user_data.get('NOMBRE_COMPLETO', ''),
            'EMAIL': user_data.get('EMAIL', ''),
            'AREA': user_data.get('AREA', ''),
            'ROL': user_data.get('ROL', 'DISEÑADOR'),
            'ESTADO': user_data.get('ESTADO', 'ACTIVO'),
            'FECHA_CREACION': user_data.get('FECHA_CREACION').isoformat() + 'Z' if user_data.get('FECHA_CREACION') else None
        }
        
        # Agregar puntuación de búsqueda si existe
        if '_searchScore' in user_data:
            formatted['_searchScore'] = user_data['_searchScore']
        
        return formatted
    
    def _format_user_for_frontend(self, user_data: Dict) -> Dict:
        """Formatea los datos del usuario para el frontend (legacy)"""
        # Adaptado para la estructura real de la tabla
        full_name = user_data.get('NOMBRE_COMPLETO', '')
        name_parts = full_name.split(' ', 1) if full_name else ['', '']
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        return {
            'id': str(user_data.get('ID_USUARIO', '')),
            'firstName': first_name,
            'lastName': last_name,
            'email': user_data.get('EMAIL', ''),
            'role': user_data.get('ROL', 'DISEÑADOR'),
            'status': user_data.get('ESTADO', 'ACTIVO'),
            'phone': '',  # No está en la estructura actual
            'department': user_data.get('AREA', ''),
            'joinedAt': user_data.get('FECHA_CREACION').isoformat() if user_data.get('FECHA_CREACION') else None,
            'lastLoginAt': None,  # No está en la estructura actual
        }