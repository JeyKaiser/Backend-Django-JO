from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, List, Optional, Tuple

import hdbcli.dbapi
from django.conf import settings

from .mock_data import (
    CONSUMO_TEXTIL,
    CONSUMOS_BY_REFERENCE,
    DIM_ANCHO_UTIL,
    DIM_BASE_TEXTIL,
    DIM_CANTIDAD_TELAS,
    DIM_CARACTERISTICA_COLOR,
    DIM_DESCRIPCION,
    DIM_PROPIEDADES_TELA,
    DIM_TERMINACION,
    DIM_USO_TELA,
    DIM_VARIANTE,
    PARAMETER_OPTIONS,
    PARAMETERS_VIEW,
    PRENDAS,
)
from .models import SapParametroRecord


class SapConfigurationError(Exception):
    pass


@dataclass
class QueryResponse:
    data: List[Dict[str, Any]]
    error: Optional[str] = None


class MockSapProvider:
    def is_available(self) -> Tuple[bool, str]:
        return True, 'SAP mock provider enabled'

    def get_prendas(self) -> List[Dict[str, Any]]:
        return PRENDAS

    def get_dimension(self, name: str) -> List[Dict[str, Any]]:
        dimensions = {
            'dim_prenda': PRENDAS,
            'dim_cantidad_telas': DIM_CANTIDAD_TELAS,
            'dim_uso_tela': DIM_USO_TELA,
            'dim_base_textil': DIM_BASE_TEXTIL,
            'dim_caracteristica_color': DIM_CARACTERISTICA_COLOR,
            'dim_ancho_util': DIM_ANCHO_UTIL,
            'dim_propiedades_tela': DIM_PROPIEDADES_TELA,
            'dim_variante': DIM_VARIANTE,
            'dim_descripcion': DIM_DESCRIPCION,
            'dim_terminacion': DIM_TERMINACION,
        }
        return dimensions.get(name, [])

    def get_parameter_options(self, name: str) -> List[Dict[str, Any]]:
        return PARAMETER_OPTIONS.get(name, [])

    def list_parametros(self) -> List[Dict[str, Any]]:
        dynamic_records = [
            {
                'CODIGO': item.codigo,
                'BASE_TEXTIL': item.base_textil,
                'TELA': item.tela,
                'ANCHO': float(item.ancho),
                'PRINT': item.print_name,
                'HILO_DE_TELA': item.hilo_de_tela,
                'HILO_DE_MOLDE': item.hilo_de_molde,
                'CANAL_TELA': item.canal_tela,
                'SENTIDO_SESGOS': item.sentido_sesgos,
                'ROTACION_MOLDE': item.rotacion_molde,
                'RESTRICCIONES_TELA': item.restricciones_tela,
                'CREATED_AT': item.created_at.isoformat(),
            }
            for item in SapParametroRecord.objects.all()
        ]
        return dynamic_records + PARAMETERS_VIEW

    def create_parametro(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        option_fields = {
            'BASE_TEXTIL_ID': ('base_textil', 'base_textil'),
            'TELA_ID': ('tela', 'tela'),
            'PRINT_ID': ('print', 'print_name'),
            'HILO_DE_TELA_ID': ('hilo_tela', 'hilo_de_tela'),
            'HILO_DE_MOLDE_ID': ('hilo_molde', 'hilo_de_molde'),
            'CANAL_TELA_ID': ('canal_tela', 'canal_tela'),
            'SENTIDO_SESGOS_ID': ('sentido_sesgos', 'sentido_sesgos'),
            'ROTACION_MOLDE_ID': ('rotacion_molde', 'rotacion_molde'),
            'RESTRICCIONES_ID': ('restricciones_tela', 'restricciones_tela'),
        }
        resolved: Dict[str, Any] = {}
        for payload_key, (source_name, target_name) in option_fields.items():
            option = next(
                (item for item in self.get_parameter_options(source_name) if item['ID'] == payload[payload_key]),
                None,
            )
            if option is None:
                raise SapConfigurationError(f'Opcion invalida para {payload_key}')
            resolved[target_name] = option['NOMBRE']

        record, _ = SapParametroRecord.objects.update_or_create(
            codigo=payload['CODIGO'],
            defaults={
                **resolved,
                'ancho': Decimal('1.50'),
            },
        )
        return {
            'success': True,
            'data': {
                'CODIGO': record.codigo,
                'BASE_TEXTIL': record.base_textil,
                'TELA': record.tela,
                'ANCHO': float(record.ancho),
                'PRINT': record.print_name,
                'HILO_DE_TELA': record.hilo_de_tela,
                'HILO_DE_MOLDE': record.hilo_de_molde,
                'CANAL_TELA': record.canal_tela,
                'SENTIDO_SESGOS': record.sentido_sesgos,
                'ROTACION_MOLDE': record.rotacion_molde,
                'RESTRICCIONES_TELA': record.restricciones_tela,
                'CREATED_AT': record.created_at.isoformat(),
            },
        }

    def get_consumos_by_reference(self, reference: str) -> List[Dict[str, Any]]:
        return CONSUMOS_BY_REFERENCE.get(reference.upper(), [])

    def create_consumo(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {'success': True, 'data': payload}

    def get_consumo_textil(self, tipo_prenda: str, cantidad_telas: Optional[int], numero_variante: Optional[str]) -> List[Dict[str, Any]]:
        results = [item for item in CONSUMO_TEXTIL if item['tipo_prenda'].lower() == tipo_prenda.lower()]
        if cantidad_telas is not None:
            results = [item for item in results if item['cantidad_telas'] == cantidad_telas]
        if numero_variante:
            results = [item for item in results if item['numero_variante'].lower() == numero_variante.lower()]
        return results

    def create_fact_consumo(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {'success': True, 'message': 'Referente guardado en modo mock', 'data': payload}


class HanaSapProvider(MockSapProvider):
    def __init__(self):
        self.config = settings.HANA_CONFIG

    def is_available(self) -> Tuple[bool, str]:
        required = ['address', 'port', 'user', 'password']
        missing = [key for key in required if not self.config.get(key)]
        if missing:
            return False, f'Faltan variables HANA: {", ".join(missing)}'
        return True, 'SAP HANA configured'

    def execute_query(self, query: str, params: Optional[List[Any]] = None) -> QueryResponse:
        ok, message = self.is_available()
        if not ok:
            return QueryResponse([], message)
        try:
            connection = hdbcli.dbapi.connect(
                address=self.config['address'],
                port=int(self.config['port']),
                user=self.config['user'],
                password=self.config['password'],
                databaseName=self.config['database'],
                encrypt=self.config.get('encrypt', True),
                sslValidateCertificate=self.config.get('sslValidateCertificate', False),
            )
            try:
                cursor = connection.cursor()
                cursor.execute(query, params or [])
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    connection.commit()
                    data = []
                return QueryResponse(data)
            finally:
                connection.close()
        except Exception as exc:
            return QueryResponse([], str(exc))

    def get_consumos_by_reference(self, reference: str) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                T3."Name" AS "COLECCION",
                T1."U_GSP_Desc" AS "NOMBRE_REF",
                T2."U_GSP_SchLinName" AS "USO_EN_PRENDA",
                T2."U_GSP_ItemCode" AS "COD_TELA",
                T2."U_GSP_ItemName" AS "NOMBRE_TELA",
                T2."U_GSP_QuantMsr" AS "CONSUMO"
            FROM "@GSP_TCMODEL" T1
            INNER JOIN "@GSP_TCMODELMAT" T2
                ON T1."Name" = T2."U_GSP_ModelCode"
            INNER JOIN "@GSP_TCCOLLECTION" T3
                ON T1."U_GSP_COLLECTION" = T3."U_GSP_SEASON"
            WHERE T1."U_GSP_REFERENCE" = ?
            AND T2."U_GSP_SchName" = 'TELAS'
            ORDER BY T2."U_GSP_SchName" DESC
        """
        response = self.execute_query(query, [reference])
        if response.error:
            return super().get_consumos_by_reference(reference)
        return response.data

    def create_consumo(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        query = """
            INSERT INTO SBOJOZF."@GSP_TCCONSUMPTION" (
                "U_GSP_REFERENCE", "U_GSP_ITEM_CODE", "U_GSP_QUANTITY", "U_GSP_UNIT"
            ) VALUES (?, ?, ?, ?)
        """
        response = self.execute_query(
            query,
            [
                payload.get('referencia'),
                payload.get('codigo_tela'),
                payload.get('cantidad_consumo'),
                payload.get('unidad_medida'),
            ],
        )
        if response.error:
            raise SapConfigurationError(response.error)
        return {'success': True, 'data': payload}


def get_provider():
    mode = getattr(settings, 'SAP_BACKEND_MODE', 'mock')
    if mode == 'hana':
        return HanaSapProvider()
    return MockSapProvider()


def execute_hana_query(query: str, params: Optional[List[Any]] = None, schema: Optional[str] = None):
    provider = get_provider()
    if isinstance(provider, MockSapProvider):
        reference = params[0] if params else None
        if 'U_GSP_REFERENCE' in query and reference:
            return provider.get_consumos_by_reference(str(reference)), None
        return [], 'La consulta SAP no esta disponible en modo mock.'

    response = provider.execute_query(query, params)
    return response.data, response.error
