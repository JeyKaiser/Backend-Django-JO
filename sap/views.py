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
    queryGetSapModels,


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
# from django.db import connection  

#from picking.packinglist.filterCharacters import filterCharacters

import time
import os
from rich.console import Console
import platform

operatingSystem = platform.system()
console = Console()

@api_view(['GET'])

def models(request):

    console.log(f"iniciando consulta a sap")
    # database = request.GET.get('database')
    database = 'SBOJOZF'
    # collection = request.GET.get('collection')
    collection = '105'

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryGetSapModels(collection))
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
    # if (len(rows) > 0):
    #     for data in rows:
    #         listData.append({
    #             'colorName': data[0]
    #         })

    #     nameColor = listData[0]['colorName']
    # else:
    #     listData = []
    cursor.close()
    return Response(data)


def modelsExample(request, collection_id):

    console.log(f"iniciando consulta a sap")
    # database = request.GET.get('database')
    # collection = request.GET.get('collection')
    database = 'SBOJOZF'
    collection = str(collection_id)
    print(f"Collection: {collection}")

    cursor = conn.cursor()
    cursor.execute(querySelectDataBase(database))
    cursor.execute(queryGetSapModels(collection))    
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

    print(rows)    
    cursor.close()    
    return data



# # @getColorItem() -> getItemColor()
# def getColorItem(colorCod, database):
#     nameColor = ""
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetItemColor(colorCod))
#     listData = []
#     rows = cursor.fetchall()
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'colorName': data[0]
#             })

#         nameColor = listData[0]['colorName']
#     else:
#         listData = []
#     cursor.close()

#     return nameColor

# def getCompositionItem(itemCode, database):
#     composition = ""
#     if itemCode[0] != "S":
#         query = queryGetCompositionItemSIIGO(itemCode)
#     else:
#         query = queryGetCompositionItemSAP(itemCode)

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(query)
#     listData = []
#     rows = cursor.fetchall()
#     #print(len(rows))
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'composition': data[0]
#             })

#         composition = listData[0]['composition']
#     else:
#         listData = []
#     cursor.close()

#     return composition


# def getTitleSaleOrder(docNum, database, OrderOrQuotation):
    
#     cursor = conn.cursor()

#     # console.log(f"Conexion de mysql estatus: {conn.get_connection()}")

#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetTitleSaleOrder(docNum, OrderOrQuotation))


#     listData = []
#     rows = cursor.fetchall()

#     cursor.execute(queryGetCollectionIDByName(rows[0][16]))
#     collectionID = ''
#     try:
#         collectionID = cursor.fetchall()[0][0]
#         # console.log(collectionID)
#     except:
#         pass
    
#     cursor.close()

#     if (len(rows) > 0):
#         for data in rows:
#             if data[3] == "C":
#                 status = "Cerrada"
#             else:
#                 status = "Abierta"
#             listData.append({
#                 'DocEntry': data[0],
#                 'DocNum': data[1],
#                 'Canceled': data[2],
#                 'DocStatus': status,
#                 'CardCode': data[4],
#                 'CardName': data[5],
#                 'DocDate': data[6],
#                 'DocDueDate': data[7],
#                 'TaxDate': data[8],
#                 'ShipToCode': data[9],
#                 'Address2': data[10],
#                 'PayToCode': data[11],
#                 'Address': data[12],
#                 'GroupNum': data[13],
#                 'Comments': data[14],
#                 'DocDueDate': data[15],
#                 'collection': data[16],
#                 'collectionId': collectionID,
#                 'U_TI_BODEGACLIENTE': data[17],
#                 'U_TI_TIENDACLIENTE': data[18],
#                 'U_TI_DEPTOCLIENTE': data[19],
#                 'DocTotalDivisa': data[20],
#                 'DocTotal': data[21],
#                 'POClient': data[22],
#             })
#             break
        
#         return listData
#     else:
#         #cursor.close()
#         return None

# def getTitleSaleQuotation(docNum, database):
    
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetTitleSaleQuotation(docNum))
#     listData = []
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         for data in rows:
#             if data[3] == "C":
#                 status = "Cerrada"
#             else:
#                 status = "Abierta"
#             listData.append({
#                 'DocEntry': data[0],
#                 'DocNum': data[1],
#                 'Canceled': data[2],
#                 'DocStatus': status,
#                 'CardCode': data[4],
#                 'CardName': data[5],
#                 'DocDate': data[6],
#                 'DocDueDate': data[7],
#                 'TaxDate': data[8],
#                 'ShipToCode': data[9],
#                 'Address2': data[10],
#                 'PayToCode': data[11],
#                 'Address': data[12],
#                 'GroupNum': data[13],
#                 'Comments': data[14],
#                 'DocDueDate': data[15],
#                 'collection': data[16],
#                 'U_TI_BODEGACLIENTE': data[17],
#                 'U_TI_TIENDACLIENTE': data[18],
#                 'U_TI_DEPTOCLIENTE': data[19],
#                 'DocTotalDivisa': data[20],
#                 'DocTotal': data[21]
#             })
#             break
        
#         return listData
#     else:
#         #cursor.close()
#         return None
    

# # REDUCIR FUNCION SE LOGRA CON UN SOLO QUERY
# # @saleOrder -> docNum (hecho)
# # @dataBase -> database (hecho)
# # @getItems_SalesOrder() -> getItemsSaleOrder
# def getItemsSaleOrder(docNum, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetItemsSaleOrder(docNum))
#     listData = []
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'ItemCode': data[0] if data[0] != None else 0,
#                 'Description': data[1] if data[1] != None else "",
#                 'Quantity': data[2] if data[2] != None else 0,
#                 'CodeBars': data[3],
#                 'WhsCode': data[4] if data[4] != None else 0,
#             })
#     else:
#         listData = []
#     #cursor.close()

#     return listData
    


# def getItemsSaleQuotation(docNum, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetItemsSaleQuotation(docNum))
#     listData = []
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         for data in rows:

#             listData.append({
#                 'ItemCode': data[0] if data[0] != None else 0,
#                 'Description': data[1] if data[1] != None else "",
#                 'Quantity': data[2] if data[2] != None else 0,
#                 'CodeBars': data[3],
#                 'WhsCode': data[4] if data[4] != None else 0,
#             })
#     else:
#         listData = []

#     return listData

# def getItemsMultipleSaleOrderOrQuotation(
#         database,
#         orderOrQuotation,
#         saleOrdersConsulta,
#         customerCodeConsulta,
#         customerConsulta,
#         collectionConsulta,
#         descriptionConsulta,
#         itemCodeConsulta,
#         quantityConsulta,
#         stateConsulta,
#     ):

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
    
#     listData = []

#     # for docNum in docNums:      
#     cursor.execute(queryGetItemsSaleOrderOrQuotation(
#         orderOrQuotation,
#         saleOrdersConsulta,
#         customerCodeConsulta,
#         customerConsulta,
#         collectionConsulta,
#         descriptionConsulta,
#         itemCodeConsulta,
#         quantityConsulta,
#         stateConsulta,
#     ))
#     rows = cursor.fetchall()

#     # console.log(rows)
#     cursor.close()

#     if (len(rows) > 0):
#         for data in rows:

#             listData.append([
#                 data[0] if data[0] != None else 0,
#                 data[1] if data[1] != None else "",
#                 data[2] if data[2] != None else 0,
#                 data[3],
#                 data[4] if data[4] != None else 0,
#                 data[5] if data[5] != None else 0,
#                 data[6] if data[6] != None else 0,
#                 data[7] if data[7] != None else 0,
#                 data[8] if data[8] != None else 0,
#                 data[9] if data[9] != None else 0,
#                 data[10] if data[10] != None else 0,
#             ])

#         listData.insert(0, ['saleOrder', 'customerCode', 'customerName', 'collection', 'itemCode', 'description', 'empacado', 'Solicitado', 'pendiente', '% completado', 'estado'])
#         return listData
#     else:
#         listData = []

#     return listData

# def getItemsSaleQuotationAndOrderImage(docNum, database, orderOrQuotation):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetItemsSaleQuotationAndOrderImage(docNum, orderOrQuotation))
#     listData = []
#     rows = cursor.fetchall()
#     cursor.close()

#     console.log(rows)

#     if (len(rows) > 0):
#         for data in rows:
#             if data[5] != None:
#                 console.log(data[5])
#                 # listaPath = data[5].replace('\\', '/')
#                 # pathdir = listaPath.rpartition(".2/")[2]
#                 #pathdir = pathdir.replace("I","i",1)  #se pone este rplace debido a que la ruta en el servidor inici con "i" minuscula, asi evitamos error

#                 try :
#                     if operatingSystem == "Linux":
#                         console.log(data[5])
#                         listaPath = data[5].replace('\\', '/')
#                         console.log(listaPath)
#                         pathdir = listaPath.rpartition(".2/")[2]
#                         imagePath = os.path.join('/', pathdir)
#                     else:
#                         pathdir = listaPath.rpartition(".2/")[2]
#                         # imagePath = os.path.join('C:/Users/USUARIO/Desktop/', pathdir)
#                         imagePath = pathdir #listaPath #pathdir
#                 except:
#                     imagePath = None
#             else:
#                     imagePath = None

#             console.log()

#             # console.log(imagePath)

#             listData.append({

#                 'ItemCode': data[0] if data[0] != None else 0,
#                 'Description': data[1] if data[1] != None else "",
#                 'Quantity': data[2] if data[2] != None else 0,
#                 'CodeBars': data[3],
#                 'WhsCode': data[4] if data[4] != None else 0,
#                 'pathFile': imagePath if imagePath != None else "",
#                 'price': data[6] if data[0] != None else 0,
#                 'currency': data[7] if data[0] != None else "",
#             })

#     else:
#         listData = []
#     #cursor.close()

#     return listData


# # Verificar donde se usa con infoReferenciaSAPitemCode y infoReferenciaSAPItemCode
# # Donde la "i" de itemCode cambia de mayuscula a minuscula
# # Ajustar!
# # @infoReferenciaSAPitemCode -> getInfoReferenceSAPitemCode() (hecho)
# def getInfoReferenceSAPitemCode(itemCode, database, docNum, orderOrQuotation):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetInfoReferenceSAPitemCode(itemCode, docNum, orderOrQuotation))
#     listData = []
#     rows = cursor.fetchall()
#     cursor.close()
#     # especificar campos
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'itemCode': data[0] if data[0] != None else 0,
#                 'itemName': data[1] if data[1] != None else 0,
#                 'barcode': data[2],
#                 'collection': data[3] if data[3] != None else 0,
#                 'price': data[4] if data[4] != None else 0,
#             })

#         #print(listData)
#         return listData[0]
#     else:
#         #cursor.close()
#         return None

    
# # @ infoReferenciaSAPcodebar() -> getInfoReferenceSAPCodebars() (hecho)
# # @ docNum se agregó docNum
# def getInfoReferenceSAPCodebars(docNum, codebars, database):

#     # especificar campos
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetInfoReferenceSAPCodebarsSaleOrder(docNum, codebars))
#     listData = []
#     rows = cursor.fetchall()
    
#     # Verificamos si hay un codigo de barras de asociado al item en el pedido de venta
#     # Si esto no ocurre llegara una lista vacia
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'itemCode': data[0],
#                 'itemName': data[1],
#                 'barcode': data[2]
#             })

#         cursor.close()
#         return listData[0]

#     # Al no haber un condigo de barras asociado a al item de la orden de venta
#     # Se procede a buscar en el maestro de articulos
#     # En caso de llegar vacia indica que no hay un item asociado al codigo de barras que ingresó le usuario
#     elif (len(rows) == 0):
#         cursor.execute(queryGetInfoReferenceSAPCodebarsItemMaster(codebars))
#         rows2 = cursor.fetchall()
#         if (len(rows2) > 0):
#             for data in rows2:
#                 listData.append({
#                     'itemCode': data[0],
#                     'itemName': data[1],
#                     'barcode': data[2]
#                 })
#             cursor.close()
#             return listData[0]
#     else:
#         # Este algoritmo prioriza el codigo de barras que tenga el item en la orden de venta
#         cursor.close()
#         return None


# def getInfoReferenceSAPCodebarsArray(database, docNum, codebars, orderOrQuotation):
#     cursor = conn.cursor()
    
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetInfoReferenceSAPCodebarsSaleOrder(docNum, codebars, orderOrQuotation))
#     listData = []
#     rows = cursor.fetchall()

#     # Verificamos si hay un codigo de barras de asociado al item en el pedido de venta
#     # Si esto no ocurre llegara una lista vacia
#     if (len(rows) > 0):
#         for data in rows:
#             reference = {
#                 'itemCode': data[0],
#                 'itemName': data[1],
#                 'barcode': data[2],
#                 'price': data[3]
#             }
#         cursor.close()
#         return reference

#     # Al no haber un codigo de barras asociado al item de la orden de venta
#     # Se procede a buscar en el maestro de articulos
#     # En caso de llegar vacia indica que no hay un item asociado al codigo de barras que ingresó le usuario
    
#     elif (len(rows) == 0):
#         cursor.execute(querySelectDataBase(database))
#         cursor.execute(queryGetInfoReferenceSAPCodebarsItemMaster(codebars))
#         rows2 = cursor.fetchall()
#         if (len(rows2) > 0):
#             for data in rows2:
#                 listData.append({
#                     'itemCode': data[0],
#                     'itemName': data[1],
#                     'barcode': data[2],
#                     'price':data[3]
#                 })
#             cursor.close()
#             return listData
#     else:
#         # Este algoritmo prioriza el codigo de barras que tenga el item en la orden de venta
#         cursor.close()
#         return None


# def statusCustomerDate(fec_desde, fec_hasta, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryStatusCustomerByDate(fec_desde, fec_hasta))
#     listData = []
#     rows = cursor.fetchall()
#     # especificar campos
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'CardName': data[0],
#                 'SUM(Quantity)': data[1],
#                 'SUM(Price*Quantity)': data[2],
#                 'Currency': data[3]
#             })
#     else:
#         listData = []
#     cursor.close()

#     return listData

# def statusCustomerCollection(collection, database):

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryStatusCustomerByCollection(collection))
#     listData = []
#     rows = cursor.fetchall()
#     # especificar campos
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'CardName': data[0],
#                 'SUM(Quantity)': data[1],
#                 'SUM(Price*Quantity)': data[2],
#                 'Currency': data[3]
#             })
#     else:
#         listData = []
#     cursor.close()

#     return listData

# def billingReport(fecini, fecfin, database):

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetInvoiceReport(fecini, fecfin))
#     listData = []
#     rows = cursor.fetchall()
#     # especificar campos

#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 "cardCode": data[0],
#                 "cardName": data[1],
#                 "itemCode":data[2],
#                 "quantity":data[3],
#                 "price":data[4],
#                 "docNum":data[5],
#                 "subpartida1":data[6],
#                 "subpartida2":data[7],
#                 "address":data[8],
#                 "taxDate":data[9],
#                 "country":data[10],
#                 "city":data[11],
#                 "moneda":data[12],
#                 "totalFact":data[13],
#                 "totalFactDivisa":data[14],
#                 "descuentoPesos":data[15],
#                 "descuentoDivisa":data[16] 
#             })
#     else:
#         listData = []
#     cursor.close()

#     return listData

# def getTotalNoItemsSaleOrder( docNum, database ):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetNumTotalItemsSaleOrder( docNum ))
#     numTotal = {}
#     rows = cursor.fetchall()
#     # especificar campos

#     if (len(rows) > 0):
#         for data in rows:
#            numTotal = {
#                'quantity': data[0]
#            }
#         cursor.close()
#         return numTotal
#     else:
#         cursor.close()
#         return None

# def getTotalNoItemsCollection(collection, database ):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetTotalNoItemsCollection( collection ))
#     numTotal = {}
#     rows = cursor.fetchall()
#     # especificar campos

#     if (len(rows) > 0):
#         numTotal = {
#             'quantity': rows[0][0]
#         }
#         cursor.close()
#         return numTotal
#     else:
#         cursor.close()
#         return None

# def getListInvoicesOfSaleOrder(docNum, company, orderOrQuotation, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))

#     console.log(company)

#     if orderOrQuotation == 'Quotation':
#         cursor.execute(queryGetListInvoicesOfSaleQuotations(docNum))
#     else:
#         cursor.execute(queryGetListInvoicesOfSaleOrder( docNum ))
#     listData = []
#     rows = cursor.fetchall()

#     console.log(rows)
#     # especificar campos
#     invoice_name = [
#         'FEZ', # Para SBOJOZF
#         'FEJC', #Para SBOJOCOL
#         'FACVTA', #Para SBOJOZFLLC
#         'FACVTA', #Para SBOJOZFLLC
#     ]
    
#     if (len(rows) > 0 ):
#         if rows[0][0] != None:
#             cont = 0
#             for data in rows:
#                 listData.append(
#                     #str(data[0]) + " " +str(data[1])
                    
#                     invoice_name[company-1]+ " " + str(data[0])
#             )
#             cont = cont + 1
#             cursor.close()
#             return listData
#     else:
#         cursor.close()
#         return None

# def getListAllCollection(database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetListAllCollection())
#     listData = []
#     rows = cursor.fetchall()
#     # especificar campos

#     if (len(rows) > 0):
#         for data in rows:
#            listData.append({
#                'Code' : data[0],
#                'Name': data[1]
#            })
#         cursor.close()
#         return listData
#     else:
#         cursor.close()
#         return None


# # def getInfoStatusPickingBilledByCardCodeAndCollection(database, collection, cardCode):
#     # cursor = conn.cursor()
#     # cursor.execute(querySelectDataBase(database))
#     # cursor.execute(queryGetInfoStatusPickingBilledByCardNameAndCollection(collection, cardCode))
#     # rows = cursor.fetchall()
#     # # especificar campos

#     # if (len(rows) > 0):
#     #     listData = {
#     #         'cardCode': rows[0][0],
#     #         'collection': rows[0][1],
#     #         'totalRecaudo': rows[0][2],
#     #         'cantidadItems': rows[0][3],
#     #     }
#     #     cursor.close()
#     #     return listData
#     # else:
#     #     cursor.close()
#     #     return None
    

# def getAllCustomer(database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetAllCustomer())
#     rows = cursor.fetchall()
#     # especificar campos
#     listData = []
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'cardCode': data[0],
#                 'cardName': data[1],
#             })
#         cursor.close()
#         return listData
#     else:
#         cursor.close()
#         return None

# def getTotalUndSaleOrdersByCustomerCodeAndCollection(database, customer, collectionId, verify):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetTotalUndSaleOrdersByCustomerCodeAndCollection(customer, collectionId, verify))
#     rows = cursor.fetchall()
#     cursor.close()

#     # especificar campos
#     listData = []
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append({
#                 'totalUnd': data[0],
#                 # 'collection': data[1],
#                 'totalFC': data[1],
#             })
        
#         return listData
#     else:
#         #cursor.close()
#         return None
    

# # def getQuantityOfItemInSaleOrder(itemCode, docNum, database):
# #     quantity = 0
# #     cursor = conn.cursor()
# #     cursor.execute(querySelectDataBase(database))
# #     cursor.execute(queryGetQuantityOfItemInSaleOrder(itemCode, docNum))
# #     rows = cursor.fetchall()
# #     # especificar campos
# #     if (len(rows) > 0):
# #         quantity = rows[0][0]
# #         cursor.close()
# #         return quantity['quantity']
# #     else:
# #         cursor.close()
# #         return None


# # este no se esta utilizando
# # def getSumDocTotalInvoicesByCustomer(database, cardCode, collectionId):
# #     listData = []
# #     cursor = conn.cursor()
# #     cursor.execute(querySelectDataBase(database))
# #     cursor.execute(queryGetInfoStatusPickingBilledByCardNameAndCollection(cardCode, collectionId))
# #     rows = cursor.fetchall()
# #     # especificar campos
# #     if (len(rows) > 0):
# #         for data in rows:
# #             listData.append({
# #                 'totalRecaudo':data[2]
# #             })
# #         cursor.close()
# #         return listData['totalRecaudo']
# #     else:
# #         cursor.close()
# #         return None


# def getSumTotalProforma(database, customerCode, collectionId):
#     quantity = 0
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSumTotalProforma(customerCode, collectionId))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         quantity = rows
#         #cursor.close()
#         return quantity
#     else:
#         #cursor.close()
#         return None


# def getSumTotalInvoice(database, customerCode, collectionId):
#     quantity = 0
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSumTotalInvoice(customerCode, collectionId))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         quantity = rows
#         #cursor.close()
#         return quantity
#     else:
#         #cursor.close()
#         return None

# def GetCountryOrigin(references, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetCountryOrigin(references))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         quantity = [i[0] for i in rows]
#         #cursor.close()
#         return quantity
#     else:
#         #cursor.close()
#         return None



# # queryGetUnitMeasure
# def getUnitMeasure(references, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetUnitMeasure(references))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         quantity = [(i[0], i[1])   for i in rows]
#         #cursor.close()
#         return quantity
#     else:
#         #cursor.close()
#         return None
# # def getSaleOrderCollection(database, orderPv, orderOrQuotation):
# #     cursor = conn.cursor()
# #     cursor.execute(querySelectDataBase(database))
# #     cursor.execute(queryGetSaleOrderCollection(orderPv, orderOrQuotation))
# #     rows = cursor.fetchall()
# #     cursor.close()

# #     if (len(rows) > 0):
# #         #cursor.close()
# #         return rows[0][0]
# #     else:
# #         #cursor.close()
# #         return None


# def getSaleOrderCollectionId(database, orderPv, orderOrQuotation):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSaleOrderCollectionId(orderPv, orderOrQuotation))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         #cursor.close()
#         return rows[0][0]
#     else:
#         #cursor.close()
#         return None


# def getSaleOrderCollectionIdByName(database, orderPv, orderOrQuotation):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSaleOrderCollectionIdByName(orderPv, orderOrQuotation))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         #cursor.close()
#         return rows[0][0]
#     else:
#         #cursor.close()
#         return None


# def getCollectionIDByName(database, collectionName):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetCollectionIDByName(collectionName))
#     rows = cursor.fetchall()
#     cursor.close()

#     if (len(rows) > 0):
#         #cursor.close()
#         return rows[0][0]
#     else:
#         #cursor.close()
#         return ''

# def getWarehouses(database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetWarehouses())
#     rows = cursor.fetchall()
#     cursor.close()

#     listData = []
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append(data[0])
        
#         return listData      
#     else:
#         return None


# def getSingleItemName(itemCode, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSingleItemName(itemCode))
#     rows = cursor.fetchall()
#     cursor.close()
#     console.log(rows)
#     console.log(rows[0][0])

#     if rows != None:
#         return rows[0][0]      
    
#     return None

# def getSingleItemNameByBarCode(itemCode, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSingleItemNameByBarCode(itemCode))
#     rows = cursor.fetchall()
#     cursor.close()
#     console.log(rows)
#     console.log(rows[0][0])

#     if rows != None:
#         return rows[0][0], rows[0][1]     
    
#     return None


# def getMultipleItemName(itemCodes, database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetMultipleItemName(itemCodes))
#     rows = cursor.fetchall()
#     cursor.close()

#     listData = []
#     if (len(rows) > 0):
#         for data in rows:
#             listData.append(data[0])
        
#         return listData      
#     else:
#         return None
    
# def getInventoryConsolidationReport(database,itemCodes, quantities, warehouse):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetInventoryConsolidationReport(itemCodes, quantities, warehouse))
#     rows = cursor.fetchall()
#     cursor.close()

#     listData = []

#     if rows:
#         for data in rows:
#             listData.append([
#                 data[0],
#                 data[1],
#                 data[2],
#                 data[3],
#             ])
        
#         return listData      
#     else:
#         return None


# def getCustomerData(database):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetCustomerData())
#     rows = cursor.fetchall()
#     cursor.close()

#     listData = []

#     if rows:
#         for data in rows:
#             listData.append(
#                 data[0],
#         #         # data[1],
#         #         # data[2],
#         #         # data[3],
#             )

        
#         return listData      
#     else:
#         return None
    

# def getStatusByseveralPickings(database, orderOrQuotation, textOrders, items, order, quantities, estadosPicking, pesoBruto, pesoNeto, dimensiones):

    

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetStatusByseveralPickings(textOrders, orderOrQuotation, items, order, quantities, estadosPicking, pesoBruto, pesoNeto, dimensiones))
#     rows = cursor.fetchall()

#     if len(rows) > 0:
#         column_names = [column[0] for column in cursor.description]
#         data = [ dict(zip(column_names, i)) for i in rows ]

#     cursor.close()

#     return data


# def dropSapContingencyTableRegisters(database): 
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     try:
#         cursor.execute(querydropSapContingencyTableRegisters())
        
#     except: 
#         pass

#     try:
#         cursor.execute(queryCreateSapContingencyTableRegisters())
#     except:
#         pass
#     cursor.close()



# def insertSapContingencyTableRegisters(
#     database,
#     pickingStatus,
#     ordenes,
#     items,
#     codigosBarras,
#     codigosBarrasCajas,
#     cantidades,
#     fechas,
#     tipoCajas,
#     Dimensiones,
#     identificadoresDespacho,
#     pesoBruto,
#     pesoNeto,
#     paisOrigen,
#     coleccion,
#     descripcion,
#     talla,
#     color,
#     cliente,
#     responsable,
#     ordenesTotales,
# ): 
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     # cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryInsertSapContingencyTableRegisters(
#         pickingStatus,
#         ordenes,
#         items,
#         codigosBarras,
#         codigosBarrasCajas,
#         cantidades,
#         fechas,
#         tipoCajas,
#         Dimensiones,
#         identificadoresDespacho,
#         pesoBruto,
#         pesoNeto,
#         paisOrigen,
#         coleccion,
#         descripcion,
#         talla,
#         color,
#         cliente,
#         responsable,
#         ordenesTotales,
#     ))
#     # rows = cursor.fetchall()
#     cursor.close()




# def getContingencyReportVsSapOrder(
#     database,
#     ordenesTotales,
# ): 
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetContingencyReportVsSapOrder(ordenesTotales))
#     rows = cursor.fetchall()
#     cursor.close()

#     listData = []

#     if rows:
#         for data in rows:
#             listData.append([
#                 data[0],
#                 data[1],
#                 data[2],
#                 data[3],
#                 data[4],
#                 data[5],
#                 data[6],
#                 data[7],
#                 data[8],
#                 data[9],
#                 data[10],
#                 data[11],
#                 data[12],
#                 data[13],
#                 data[14],
#                 filterCharacters(data[15]),
#                 data[16],
#                 data[17],
#                 data[18],
#                 data[19],
#                 data[20],
#             ])
        
#         return listData      
#     else:
#         return None


# def getOrdersOrQuotationsWithItemsOfCollection(database, collection, orderOrQuotation, excluirOfertasCanceladas):
#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetOrdersOrQuotationsWithItemsOfCollection(collection, orderOrQuotation, excluirOfertasCanceladas))
#     rows = cursor.fetchall()
#     cursor.close()

#     data = [ i[0] for i in rows ]

#     return data


# def getStatusByseveralCollectionOrders(database, orderOrQuotation, textOrders, items, order, quantities, estadosPicking):

    

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetStatusByseveralCollectionOrders(textOrders, orderOrQuotation, items, order, quantities, estadosPicking))
#     rows = cursor.fetchall()

#     if len(rows) > 0:
#         column_names = [column[0] for column in cursor.description]
#         data = [ dict(zip(column_names, i)) for i in rows ]

#     cursor.close()

#     return data


# def getSaleOrderOrQuotationInformation(database, originOrder, pvOrder, orderOrQuotation, itemCodes, quantities):

    

#     cursor = conn.cursor()
#     cursor.execute(querySelectDataBase(database))
#     cursor.execute(queryGetSaleOrderOrQuotationInformation(originOrder, pvOrder, orderOrQuotation, itemCodes, quantities))
#     rows = cursor.fetchall()

#     if len(rows) > 0:
#         column_names = [column[0] for column in cursor.description]
#         data = [ dict(zip(column_names, i)) for i in rows ]

#     cursor.close()

#     return data