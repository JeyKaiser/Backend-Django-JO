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
    queryReferenciasPorAno,
    queryTelasPorReferencia,
    queryInsumosPorReferencia,

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
logger = logging.getLogger(__name__)
import time
import os
from rich.console import Console
import platform
from rest_framework.views import APIView


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



def telasPorReferencia(request, referencia_id): # Cambiado collection_id por referencia_id para claridad
    logger.info(f"Buscando telas en la Base de datos para referencia: {referencia_id}")

    # Obtener collectionId de los parámetros de la URL (query parameters)
    collection_id = request.GET.get('collectionId')
    if not collection_id:
        logger.error("Django [telasPorReferencia]: collectionId no proporcionado en los query parameters.")
        # Podrías lanzar una excepción o devolver un error aquí si collectionId es obligatorio
        return [] # O manejar el error de otra manera

    database = 'SBOJOZF'
    # La variable 'collection' ahora es el collection_id que viene de Next.js
    # y se usará en la consulta SQL junto con referencia_id (ptCode)
    collection = str(collection_id)
    ptCode = str(referencia_id) # El referencia_id de la URL es el ptCode

    logger.info(f"Referencia (ptCode): {ptCode}, Colección: {collection}")

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database)) # Asegúrate de que esta función existe y es accesible

    # Llama a queryTelasPorReferencia con AMBOS parámetros
    cursor.execute(queryTelasPorReferencia(ptCode, collection))
    rows = cursor.fetchall()
    data = []

    if len(rows) > 0:
        column_names = [column[0] for column in cursor.description]
        for row in rows:
            item = dict(zip(column_names, row))
            # No hay U_GSP_Picture en la consulta de telas, así que esta parte ya no es necesaria
            # Si tu consulta de telas tuviera una columna de imagen, la lógica sería similar
            data.append(item)

    logger.debug(f"Datos raw obtenidos de la DB (antes de procesar): {rows}")
    logger.info(f"Datos procesados a devolver a Next.js: {data}")
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
    # Llama a la nueva consulta de insumos
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
