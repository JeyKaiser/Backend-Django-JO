from time import time
from .HANA.conf import conn
from .HANA.queries import (
    queryGetAllCustomer, queryGetCompositionItemSAP,
    queryGetCompositionItemSIIGO,
    queryGetSumTotalInvoice, 
    queryGetSumTotalProforma,    
    queryGetInfoReferenceSAPCodebarsItemMaster, 
    queryGetInfoReferenceSAPCodebarsSaleOrder
)

from .HANA.queries import (
    querySelectDataBase,
    queryReferenciasPorAnio,
    queryTelasPorReferencia,
    queryInsumosPorReferencia,
    querySearchPTCode,    

    queryGetInfoReferenceSAPitemCode,
    # queryGetInfoStatusPickingBilledByCardNameAndCollection,
    queryGetInvoiceReport,queryGetItemColor,
    queryGetListAllCollection,queryGetListInvoicesOfSaleOrder,
    queryGetNumTotalItemsSaleOrder,
    # queryGetQuantityOfItemInSaleOrder,
    queryGetTitleSaleOrder,
    queryGetTitleSaleQuotation,
    queryGetItemsSaleOrder,
    queryGetItemsSaleQuotation,queryGetItemsSaleQuotationAndOrderImage,
    queryGetTotalNoItemsCollection,
    queryGetTotalUndSaleOrdersByCustomerCodeAndCollection,
    querySelectDataBase,
    queryStatusCustomerByCollection,
    queryStatusCustomerByDate,queryGetCountryOrigin,
    dropTemporaryColumn,
    # queryGetSaleOrderCollection,
    queryGetWarehouses,
    queryGetSingleItemName,
    queryGetMultipleItemName, 
    queryGetInventoryConsolidationReport,
    queryGetItemsSaleOrderOrQuotation,
    queryGetListInvoicesOfSaleQuotations,
    queryGetCustomerData,
    queryGetSaleOrderCollectionId,
    queryGetCollectionIDByName,
    queryGetSingleItemNameByBarCode,
    queryGetStatusByseveralPickings,
    queryGetContingencyReportVsSapOrder,
    queryGetOrdersOrQuotationsWithItemsOfCollection,
    queryGetStatusByseveralCollectionOrders,
    queryInsertSapContingencyTableRegisters,
    querydropSapContingencyTableRegisters,
    queryCreateSapContingencyTableRegisters,
    queryGetSaleOrderOrQuotationInformation,
    queryGetUnitMeasure,
)#from .HANA.queries import queryGetTotalUndSaleOrdersByCustomerCodeAndCollection2, queryGetSumTotalInvoice2, queryGetSumTotalProforma2


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
import logging 
from rich.console import Console
import platform
from rest_framework.views import APIView
from rest_framework import status


logger = logging.getLogger(__name__)

operatingSystem = platform.system()
console = Console()

STANDARD_FASES_DISPONIBLES = [
    {"slug": "jo", "nombre": "JO"},
    {"slug": "md-creacion-ficha", "nombre": "MD CREACION FICHA"},
    {"slug": "md-creativo", "nombre": "MD CREATIVO"},
    {"slug": "md-corte", "nombre": "MD CORTE"},
    {"slug": "md-confeccion", "nombre": "MD CONFECCION"},
    {"slug": "md-fitting", "nombre": "MD FITTING"},
    {"slug": "md-tecnico", "nombre": "MD TECNICO"},
    {"slug": "md-trazador", "nombre": "MD TRAZADOR"},
    {"slug": "costeo", "nombre": "COSTEO"},
    {"slug": "pt-tecnico", "nombre": "PT TECNICO"},
    {"slug": "pt-cortador", "nombre": "PT CORTADOR"},
    {"slug": "pt-fitting", "nombre": "PT FITTING"},
    {"slug": "pt-trazador", "nombre": "PT TRAZADOR"},
]




#---------------------------------------------------------------------------------------------------
def referenciasPorAnio(collection_id):
    logger.info(f"iniciando consulta a sap para coleccion_id {collection_id}")
    database = 'SBOJOZF'
    collection = str(collection_id)
    print(f"Collection: {collection}")

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryReferenciasPorAnio(collection)) # Usamos 'collection' aquí
    rows = cursor.fetchall()

    data = []
    if len(rows) > 0:
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            item = dict(zip(column_names, row))
            picture = item.get("U_GSP_Picture")
            if picture is not None:
                picture = picture.replace("\\", "/")
                item["U_GSP_Picture"] = "https://johannaortiz.net/media/ImagesJOServer/" + picture
            data.append(item)

    logger.debug(f"Datos raw obtenidos de la DB (antes de procesar): {rows}")
    logger.info(f"Datos procesados a devolver a Next.js: {data}")
    cursor.close()
    return data



# def telasPorReferencia(request, referencia_id):
#     logger.info(f"Buscando telas en la Base de datos para referencia: {referencia_id}")
#     collection_id = request.GET.get('collectionId')
#     print(f"Collection ID usado: {collection_id}")
    
#     if not collection_id:
#         logger.error("Django [telasPorReferencia]: collectionId no proporcionado en los query parameters.")
#         return []

#     database = 'SBOJOZF'
#     collection = str(collection_id)
#     ptCode = str(referencia_id)

#     logger.info(f"Referencia (ptCode): {ptCode}, Colección: {collection}")

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryTelasPorReferencia(ptCode, collection))
#     rows = cursor.fetchall()
#     data = []

#     if len(rows) > 0:
#         column_names = [column[0] for column in cursor.description]
#         for row in rows:
#             item = dict(zip(column_names, row))
#             data.append(item)

#     logger.debug(f"Datos raw obtenidos de la DB (telas - antes de procesar): {rows}")
#     logger.info(f"Datos procesados a devolver a Next.js (telas): {data}")
#     cursor.close()
#     return data
# def insumosPorReferencia(request, referencia_id):
#     logger.info(f"Buscando insumos en la Base de datos para referencia: {referencia_id}")
#     collection_id = request.GET.get('collectionId')
#     if not collection_id:
#         logger.error("Django [insumosPorReferencia]: collectionId no proporcionado en los query parameters.")
#         return []

#     database = 'SBOJOZF'
#     collection = str(collection_id)
#     ptCode = str(referencia_id)

#     logger.info(f"Referencia (ptCode): {ptCode}, Colección: {collection}")

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryInsumosPorReferencia(ptCode, collection))
#     rows = cursor.fetchall()
#     data = []

#     if len(rows) > 0:
#         column_names = [column[0] for column in cursor.description]
#         for row in rows:
#             item = dict(zip(column_names, row))
#             data.append(item)

#     logger.debug(f"Datos raw obtenidos de la DB (insumos - antes de procesar): {rows}")
#     logger.info(f"Datos procesados a devolver a Next.js (insumos): {data}")
#     cursor.close()
#     return data

def telasPorReferencia(request, referencia_id, collection_id):
    logger.info(f"Buscando telas en la Base de datos para referencia: {referencia_id}, Colección: {collection_id}")
    # Ya no necesitamos request.GET.get('collectionId')
    # print(f"Collection ID usado: {collection_id}") # Para depuración

    # La validación de collection_id ya no es necesaria aquí si es un parámetro de ruta garantizado
    # if not collection_id:
    #     logger.error("Django [telasPorReferencia]: collectionId no proporcionado o derivado.")
    #     return []

    database = 'SBOJOZF'
    collection = str(collection_id) # Usa el collection_id que se recibió directamente
    ptCode = str(referencia_id)

    cursor = conn.cursor() # Asume que 'conn' es tu conexión a la DB
    cursor.execute(querySelectDataBase(database)) # Asume que esta función existe
    cursor.execute(queryTelasPorReferencia(ptCode, collection)) # Asume que esta función existe
    rows = cursor.fetchall()
    data = []

    if len(rows) > 0:
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            item = dict(zip(column_names, row))
            data.append(item)

    logger.debug(f"Datos raw obtenidos de la DB (telas - antes de procesar): {rows}")
    logger.info(f"Datos procesados a devolver a Next.js (telas): {data}")
    cursor.close()
    return data

# *** CAMBIO CLAVE: collection_id ahora es un parámetro directo ***
def insumosPorReferencia(request, referencia_id, collection_id):
    logger.info(f"Buscando insumos en la Base de datos para referencia: {referencia_id}, Colección: {collection_id}")
    
    database = 'SBOJOZF'
    collection = str(collection_id) # Usa el collection_id que se recibió directamente
    ptCode = str(referencia_id)

    cursor = conn.cursor() # Asume que 'conn' es tu conexión a la DB
    cursor.execute(querySelectDataBase(database)) # Asume que esta función existe
    cursor.execute(queryInsumosPorReferencia(ptCode, collection)) # Asume que esta función existe
    rows = cursor.fetchall()
    data = []

    if len(rows) > 0:
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            item = dict(zip(column_names, row))
            data.append(item)

    logger.debug(f"Datos raw obtenidos de la DB (insumos - antes de procesar): {rows}")
    logger.info(f"Datos procesados a devolver a Next.js (insumos): {data}")
    cursor.close()
    return data



def getModeloDetalle(request, referencia_id):
    logger.info(f"Obteniendo detalle completo del modelo para referencia: {referencia_id}")
    print(f"Referencia ID: {referencia_id} - Colección ID: {request.GET.get('collectionId')}")
    
    combined_data = {    
        'nombre': f"Referencia {referencia_id}",   
        'fases_disponibles': STANDARD_FASES_DISPONIBLES 
    }
    
    logger.info(f"Datos combinados del modelo para {referencia_id}: {combined_data}")
    return combined_data






class TelasAPIView(APIView):
    def get(self, request, referencia_id):
        logger.info(f"Django [TelasAPIView]: Solicitud GET recibida para referencia_id: {referencia_id}")
        try:
            # Pasa el objeto request completo a telasPorReferencia para que pueda acceder a los query params
            data_from_db = telasPorReferencia(request, referencia_id)
            return Response(data_from_db, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Django [TelasAPIView]: ERROR al obtener TELAS para la referencia '{referencia_id}': {e}", exc_info=True)
            return Response({'detail': f'Error al obtener referencias: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








# NUEVA FUNCIÓN para buscar PT Code
def searchPTCode(pt_code):
    logger.info(f"Buscando PT Code en la Base de datos: {pt_code}")

    database = 'SBOJOZF' # Tu base de datos
    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))

    # Llama a la nueva consulta de búsqueda
    cursor.execute(querySearchPTCode(pt_code))
    row = cursor.fetchone() # Usamos fetchone() porque buscamos el primer match

    search_result = None
    if row:
        column_names = [column[0] for column in cursor.description]
        # Creamos un diccionario con el resultado
        search_result = dict(zip(column_names, row))
        logger.info(f"PT Code '{pt_code}' encontrado: {search_result}")
    else:
        logger.info(f"PT Code '{pt_code}' no encontrado en la base de datos.")

    cursor.close()
    return search_result # Devolverá un diccionario o None


def models(request):                #consulta GET
    console.log(f"iniciando consulta a sap")
    # database = request.GET.get('database')
    database = 'SBOJOZF'
    # collection = request.GET.get('collection')
    collection = '105'

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryReferenciasPorAnio(collection))
    # listData = []
    rows = cursor.fetchall()

    if len(rows) > 0:
        column_names = [column[0] for column in cursor.description]
        data = []

        for row in rows:
            item = dict(zip(column_names, row))
            picture = item.get("U_GSP_Picture")
            if picture is not None:
                picture = picture.replace("\\", "/")
                item["U_GSP_Picture"] = "https://johannaortiz.net/media/ImagesJOServer/" + picture
            data.append(item)

    console.log(rows)   
    cursor.close()
    return Response(data)

