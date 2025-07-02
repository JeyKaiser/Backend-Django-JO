from time import time
from .HANA.conf import conn
from .HANA.queries import (
    queryGetAllCustomer, queryGetCompositionItemSAP,
    queryGetCompositionItemSIIGO, queryGetSumTotalInvoice, queryGetSumTotalProforma
)
from .HANA.queries import (
    queryGetInfoReferenceSAPCodebarsItemMaster, queryGetInfoReferenceSAPCodebarsSaleOrder
)
from .HANA.queries import (
    querySelectDataBase,
    queryReferenciasPorAno,
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
import time
import os
from rich.console import Console
import platform
from rest_framework.views import APIView
from rest_framework import status
logger = logging.getLogger(__name__)


operatingSystem = platform.system()
console = Console()
@api_view(['GET'])

#---------------------------------------------------------------------------------------------------
def models(request):                #consulta GET
    console.log(f"iniciando consulta a sap")
    # database = request.GET.get('database')
    database = 'SBOJOZF'
    # collection = request.GET.get('collection')
    collection = '105'

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryReferenciasPorAno(collection))
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



def referenciasPorAno(request, collection_id):
    console.log(f"iniciando consulta a sap para colecccion_id {collection_id}")    
    database = 'SBOJOZF'
    collection = str(collection_id)
    print(f"Collection: {collection}")

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryReferenciasPorAno(collection))    
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
    # print(rows)    
    cursor.close()    
    return data



def telasPorReferencia(request, referencia_id):
    logger.info(f"Buscando telas en la Base de datos para referencia: {referencia_id}")
    collection_id = request.GET.get('collectionId')
    if not collection_id:
        logger.error("Django [telasPorReferencia]: collectionId no proporcionado en los query parameters.")
        return []

    database = 'SBOJOZF'
    collection = str(collection_id)
    ptCode = str(referencia_id)

    logger.info(f"Referencia (ptCode): {ptCode}, Colección: {collection}")

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryTelasPorReferencia(ptCode, collection))
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


def insumosPorReferencia(request, referencia_id):
    logger.info(f"Buscando insumos en la Base de datos para referencia: {referencia_id}")
    collection_id = request.GET.get('collectionId')
    if not collection_id:
        logger.error("Django [insumosPorReferencia]: collectionId no proporcionado en los query parameters.")
        return []

    database = 'SBOJOZF'
    collection = str(collection_id)
    ptCode = str(referencia_id)

    logger.info(f"Referencia (ptCode): {ptCode}, Colección: {collection}")

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryInsumosPorReferencia(ptCode, collection))
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


# --- NUEVA FUNCIÓN COMBINADA ---
def getModeloDetalle(request, referencia_id):
    logger.info(f"Obteniendo detalle completo del modelo para referencia: {referencia_id}")
    
    # Reutiliza las funciones existentes para obtener los datos
    telas_data = telasPorReferencia(request, referencia_id)
    insumos_data = insumosPorReferencia(request, referencia_id)

    # Combina los resultados en un solo diccionario
    combined_data = {
        'telas': telas_data,
        'insumos': insumos_data
    }
    
    logger.info(f"Datos combinados del modelo para {referencia_id}: {combined_data}")
    return combined_data


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


