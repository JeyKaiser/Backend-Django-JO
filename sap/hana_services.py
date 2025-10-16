from sap.views import execute_hana_query
from sap.queries import (
    queryGetCollections,
    queryInsertCollection,
    queryGetTraceability,
    queryUpdateTraceability,
    queryGetCurrentTraceability,
    queryGetPhaseByCode,
    queryGetAllPhases,
    queryInsertReference,
    queryGetReferenceDetail,
    querySearchReference,
    queryGetReferencesByYear,
    queryTelasPorReferencia,
    queryInsumosPorReferencia
)
import logging

logger = logging.getLogger(__name__)

def get_collections_service():
    query = queryGetCollections()
    data, error = execute_hana_query(query)
    if error:
        logger.error(f"Error in get_collections_service: {error}")
    return data, error

def create_collection_service(code, name, season):
    query = queryInsertCollection()
    _, error = execute_hana_query(query, params=(code, name, season))
    if error:
        logger.error(f"Error in create_collection_service: {error}")
    return error

def get_traceability_service(id_referencia):
    query = queryGetTraceability()
    data, error = execute_hana_query(query, params=(id_referencia,))
    if error:
        logger.error(f"Error in get_traceability_service: {error}")
    return data, error

def update_traceability_service(id_fase, id_referencia):
    query = queryUpdateTraceability()
    _, error = execute_hana_query(query, params=(id_fase, id_referencia))
    if error:
        logger.error(f"Error in update_traceability_service: {error}")
    return error

def get_current_traceability_service(id_referencia):
    query = queryGetCurrentTraceability()
    data, error = execute_hana_query(query, params=(id_referencia,))
    if error:
        logger.error(f"Error in get_current_traceability_service: {error}")
    return data, error

def get_phase_by_code_service(codigo_fase):
    query = queryGetPhaseByCode()
    data, error = execute_hana_query(query, params=(codigo_fase,))
    if error:
        logger.error(f"Error in get_phase_by_code_service: {error}")
    return data, error

def get_all_phases_service():
    query = queryGetAllPhases()
    data, error = execute_hana_query(query)
    if error:
        logger.error(f"Error in get_all_phases_service: {error}")
    return data, error

def create_reference_service(codigo_referencia, id_coleccion, nombre_referencia):
    query = queryInsertReference()
    _, error = execute_hana_query(query, params=(codigo_referencia, id_coleccion, nombre_referencia))
    if error:
        logger.error(f"Error in create_reference_service: {error}")
    return error

def get_reference_detail_service(codigo_referencia):
    query = queryGetReferenceDetail()
    data, error = execute_hana_query(query, params=(codigo_referencia,))
    if error:
        logger.error(f"Error in get_reference_detail_service: {error}")
    return data, error

def search_reference_service(search_term):
    query = querySearchReference()
    params = (f'%{search_term}%', f'%{search_term}%')
    data, error = execute_hana_query(query, params=params)
    if error:
        logger.error(f"Error in search_reference_service: {error}")
    return data, error

def get_references_by_year_service(collection_id):
    query = queryGetReferencesByYear()
    data, error = execute_hana_query(query, params=(collection_id,))
    if error:
        logger.error(f"Error in get_references_by_year_service: {error}")
    return data, error

def get_telas_por_referencia_service(referencia_id, collection_id):
    logger.info(f"Buscando telas para referencia: {referencia_id}, Colección: {collection_id}")
    query = queryTelasPorReferencia()
    data, error = execute_hana_query(query, (referencia_id, collection_id))
    if error:
        logger.error(f"Error in get_telas_por_referencia_service: {error}")
    return data, error

def get_insumos_por_referencia_service(referencia_id, collection_id):
    logger.info(f"Buscando insumos para referencia: {referencia_id}, Colección: {collection_id}")
    query = queryInsumosPorReferencia()
    data, error = execute_hana_query(query, (referencia_id, collection_id))
    if error:
        logger.error(f"Error in get_insumos_por_referencia_service: {error}")
    return data, error