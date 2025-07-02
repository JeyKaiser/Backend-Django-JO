
import time
import logging
from rich.console import Console

console = Console()
saleOrderDbs= ("ORDR","RDR1")   # Tablas de bases de datos de orden de venta
saleQuotationDbs = ("OQUT", "QUT1")  #Tablas de bases de datos de oferta de venta
logger = logging.getLogger(__name__)


def queryReferenciasPorAno(collection):
    query = f"""
        SELECT  "U_GSP_REFERENCE", "U_GSP_Picture","U_GSP_Desc"  
        FROM "@GSP_TCMODEL" T0
        WHERE U_GSP_COLLECTION = '{collection}'
        AND LEFT(T0.U_GSP_REFERENCE, 2) IN ('PT')
        ORDER BY T0.U_GSP_REFERENCE ASC;
    """
    console.log(query)
    return query


def queryTelasPorReferencia(ptCode, collection): # Ahora acepta ambos parámetros
    query = f"""
        SELECT
        T1."U_GSP_REFERENCE",
        T2."U_GSP_SchLinName",
        T2."U_GSP_ItemCode",
        T2."U_GSP_ItemName",
        T3."BWidth1"
        FROM SBOJOZF."@GSP_TCMODEL" T1
        INNER JOIN SBOJOZF."@GSP_TCMODELMAT" T2
            ON T1."Code" = T2."U_GSP_ModelCode"
        INNER JOIN SBOJOZF."OITM" T3
            ON T2."U_GSP_ItemCode" = T3."ItemCode"
        WHERE T1."U_GSP_REFERENCE" = '{ptCode}'
            AND T1."U_GSP_COLLECTION" = '{collection}'
            AND LEFT (T2."U_GSP_ItemCode", 3) IN ('TEN','TE0')
        ORDER BY "U_GSP_SchLinName" DESC;"""
    logger.info(f"Consulta SQL generada para telas: {query}")
    return query


def queryInsumosPorReferencia(ptCode, collection):
    query = f"""
        SELECT
        T1."U_GSP_REFERENCE",
        T2."U_GSP_SchLinName",
        T2."U_GSP_ItemCode",
        T2."U_GSP_ItemName",
        T3."BWidth1" -- T3.* si quieres todas las columnas de OITM, pero solo BWidth1 fue especificado
        FROM SBOJOZF."@GSP_TCMODEL" T1
        INNER JOIN SBOJOZF."@GSP_TCMODELMAT" T2
            ON T1."Code" = T2."U_GSP_ModelCode"
        INNER JOIN SBOJOZF."OITM" T3
            ON T2."U_GSP_ItemCode" = T3."ItemCode"
        WHERE T1."U_GSP_REFERENCE" = '{ptCode}'
            AND T1."U_GSP_COLLECTION" = '{collection}'
            AND LEFT (T2."U_GSP_ItemCode", 3) IN ('INN','IN0') -- Condición específica para insumos
        ORDER BY "U_GSP_SchLinName" DESC;"""
    logger.info(f"Consulta SQL generada para insumos: {query}")
    return query


def querySelectDataBase(database):
    query = 'SET SCHEMA "' + database + '";'
    return query

# NUEVA FUNCIÓN DE CONSULTA PARA BUSCAR PT CODE
def querySearchPTCode(ptCode):  
    upper_ptCode = ptCode.upper()  
    query = f"""
        SELECT TOP 1
        "U_GSP_REFERENCE",
        "U_GSP_COLLECTION"
        FROM SBOJOZF."@GSP_TCMODEL"
        WHERE UPPER("U_GSP_REFERENCE") = '{upper_ptCode}'
        ORDER BY "U_GSP_COLLECTION" DESC;"""
    logger.info(f"Consulta SQL generada para búsqueda de PT Code: {query}")
    return query

# CONSULTA PARA OBTENER EL NOMBRE DE LA COLECCIÓN
def queryGetCollectionName(collectionId):
    query = f"""
        SELECT "Name"
        FROM SBOJOZF."@GSP_TCCOLLECTION"
        WHERE "Code" = '{collectionId}';
    """
    logger.info(f"Consulta SQL generada para obtener nombre de colección: {query}")
    return query

































def queryLastRowReferences(days):
    query = """
        SELECT 
            "ItemCode", 
            "U_TI_CODESIIGO", 
            "ItemName", 
            "InvntryUom", 
            "BuyUnitMsr" 
        FROM 
            "OITM" 
        WHERE 
            "CreateDate" >= add_days(CURRENT_DATE, -""" + str(days) + """);"""

    return query


def queryGetItemColor(colorCod):
    query = f"""
        SELECT 
            "U_GSP_Name" 
        FROM 
            "@GSP_TCCOLOR" 
        WHERE 
            "U_GSP_Code" = '{colorCod}' LIMIT 1;"""

    return query


def queryGetCompositionItemSIIGO(itemCode):
    query = """
        SELECT
            REPLACE(
                IFNULL(T24."U_DESCINITDESC", '') || ' ' || IFNULL(T24."U_COMPDESC1", '') || ' ' || IFNULL(T24."U_COMPCODE1", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP1", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC2", '') || ' ' || IFNULL(T24."U_COMPCODE2", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP2", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC3", '') || ' ' || IFNULL(T24."U_COMPCODE3", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP3", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC4", '') || ' ' || IFNULL(T24."U_COMPCODE4", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP4", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC5", '') || ' ' || IFNULL(T24."U_COMPCODE5", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP5", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC6", '') || ' ' || IFNULL(T24."U_COMPCODE6", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP6", 3, 2), 0) || '% ' || IFNULL(T24."U_DESCENDDESC", ''),
                '  0.00%',
                ''
            ) AS "REF_PT"
        FROM
            "@TI_COMPOSITION_DOC" T24
        WHERE T24."U_REFDESC" = "SPLIT_WITH_DELIMITER"('""" + itemCode + """', '_',1)"""
    
    return query


def queryGetCompositionItemSAP(itemCode):
    query = """
        SELECT
            REPLACE(
                IFNULL(T23."U_Ti_CODEDESCINITIAL", '') || ' ' || IFNULL(TO_DECIMAL(T23."U_TI_PORCENTCOMP1", 3, 2), 0) || '% ' || IFNULL(T23."U_TI_COMPCODE1", '') || ' ' || IFNULL(TO_DECIMAL(T23."U_TI_PORCENTCOMP2", 3, 2), 0) || '% ' || IFNULL(T23."U_TI_COMPCODE2", '') || ' ' || IFNULL(TO_DECIMAL(T23."U_TI_PORCENTCOMP3", 3, 2), 0) || '% ' || IFNULL(T23."U_TI_COMPCODE3", '') || ' ' || IFNULL(TO_DECIMAL(T23."U_TI_PORCENTCOMP4", 3, 2), 0) || '% ' || IFNULL(T23."U_TI_COMPCODE4", '') || ' ' || IFNULL(TO_DECIMAL(T23."U_TI_PORCENTCOMP5", 3, 2), 0) || '% ' || IFNULL(T23."U_TI_COMPCODE5", '') || ' ' || IFNULL(TO_DECIMAL(T23."U_TI_PORCENTCOMP6", 3, 2), 0) || '% ' || IFNULL(T23."U_TI_COMPCODE6", '') || ' ' || IFNULL(T23."U_TI_CODDESCEND", ''),
                '  0.00%',
                ''
            ) AS "REF_SALINI"
        FROM
            "OITM" T23
        WHERE
            T23."ItemCode" = '"""+itemCode+"""';"""

    return query


def queryGetTitleSaleOrder(docNum, orderOrQuotation):
    
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

    query = f"""
        SELECT
            T0."DocEntry",
            T0."DocNum",
            T0."CANCELED",
            T0."DocStatus",
            T0."CardCode",
            T0."CardName",
            T0."DocDate",
            T0."DocDueDate",
            T0."TaxDate",
            T0."ShipToCode",
            T0."Address2",
            T0."PayBlckRef",
            T0."Address",
            T0."GroupNum",
            T0."Comments",
            T0."DocDueDate",
            (
            SELECT 
                MAX(C."Name") 
            FROM 
                "{queryDbs[1]}" A
                INNER JOIN "OITM" B ON A."ItemCode" = B."ItemCode"
                INNER JOIN "@GSP_TCCOLLECTION" C ON B."U_GSP_COLLECTION" = C."Code"
                INNER JOIN "{queryDbs[0]}" D ON A."DocEntry" = D."DocEntry"
            WHERE D."DocNum" = '{docNum}'
            ) AS "Coleccion",
            T0."U_TI_BODEGACLIENTE",
            T0."U_TI_TIENDACLIENTE",
            T0."U_TI_DEPTOCLIENTE",
            T0."DocTotalFC",
            T0."DocTotal",
            T0."U_TI_POCLIENT"

        FROM
            "{queryDbs[0]}" T0
            INNER JOIN "{queryDbs[1]}" T1 ON T0."DocEntry" = T1."DocEntry"
            INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
        WHERE T0."DocNum" = '{docNum}';
    """

    # console.log(query)
    return query


def queryGetTitleSaleQuotation(docNum):
    query = f"""
        SELECT
            T0."DocEntry",
            T0."DocNum",
            T0."CANCELED",
            T0."DocStatus",
            T0."CardCode",
            T0."CardName",
            T0."DocDate",
            T0."DocDueDate",
            T0."TaxDate",
            T0."ShipToCode",
            T0."Address2",
            T0."PayBlckRef",
            T0."Address",
            T0."GroupNum",
            T0."Comments",
            T0."DocDueDate",
            (
            SELECT 
                MAX(C."Name") 
            FROM 
                "QUT1" A
                INNER JOIN "OITM" B ON A."ItemCode" = B."ItemCode"
                INNER JOIN "@GSP_TCCOLLECTION" C ON B."U_GSP_COLLECTION" = C."Code"
                INNER JOIN "OQUT" D ON A."DocEntry" = D."DocEntry"
            WHERE D."DocNum" = '{docNum}''
            ) AS "Coleccion",
            T0."U_TI_BODEGACLIENTE",
            T0."U_TI_TIENDACLIENTE",
            T0."U_TI_DEPTOCLIENTE",
            T0."DocTotalFC",
            T0."DocTotal",
            (
            SELECT 
                MAX(C."Code")
            FROM 
                "{queryDbs[1]}" A
                INNER JOIN "OITM" B ON A."ItemCode" = B."ItemCode"
                INNER JOIN "@GSP_TCCOLLECTION" C ON B."U_GSP_COLLECTION" = C."Code"
                INNER JOIN "{queryDbs[0]}" D ON A."DocEntry" = D."DocEntry"
            WHERE D."DocNum" = '{docNum}'
            ) AS "ColeccionId"
        FROM
            "OQUT" T0
            INNER JOIN "QUT1" T1 ON T0."DocEntry" = T1."DocEntry"
            INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
        WHERE T0."DocNum" = '{docNum}';
    """
    return query


def queryGetInfoReferenceSAPitemCode(itemCode, docNum, orderOrQuotation):
    saleOrderDbs= ("ORDR","RDR1")
    saleQuotationDbs = ("OQUT", "QUT1")
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs
    query = f"""
        SELECT 
            T0."ItemCode",
            T0."ItemName", 
            T0."CodeBars",
            T0."U_GSP_COLLECTION",
            T2."Price"
        FROM 
            "OITM" T0
            INNER JOIN {queryDbs[0]} T1 ON T1."DocNum" = '{docNum}'
            INNER JOIN {queryDbs[1]} T2 ON T1."DocEntry" = T2."DocEntry" AND T0."ItemCode" = T2."ItemCode"
        WHERE
            T0."ItemCode" = '{itemCode}';
    """
    return query


def queryGetInfoReferenceSAPCodebarsItemMaster(codebars):
    query = """
    SELECT 
        "ItemCode", 
        "ItemName", 
        "CodeBars",
        T2."Price",
        T0."U_GSP_COLLECTION"
    FROM 
        "OITM" T0
        INNER JOIN "ORDR" T1 ON T1."DocNum" = 
        INNER JOIN "RDR1" T2 ON T1."DocEntry" = T2."DocEntry" AND T0."ItemCode" = T1."ItemCode"
    WHERE 
        T0."CodeBars" = '"""+codebars+"""';
    """
    
    return query


def queryGetItemsSaleOrder(docNum):
    query = f"""
        SELECT 
            T0."ItemCode", 
            T0."Dscription", 
            T0."Quantity", 
            T2."CodeBars",
            T3."WhsCode"
        FROM 
            "RDR1" T0
            INNER JOIN "ORDR" T1 ON T0."DocEntry" = T1."DocEntry"
            INNER JOIN "OITM" T2 ON T0."ItemCode" = T2."ItemCode"
            LEFT JOIN "WTR1" T3 ON (T0."ItemCode" = T3."ItemCode" AND T1."DocNum" = T3."U_TI_ORDENVENTA")
        WHERE
        T1."DocNum" = '{docNum}'
        ORDER BY
            T0."ItemCode",
            T0."Dscription";
    """
    return query


def queryGetItemsSaleQuotation(docNum):
    query = f"""
        SELECT 
            T0."ItemCode", 
            T0."Dscription", 
            T0."Quantity", 
            T2."CodeBars",
            T3."WhsCode"
        FROM 
            "QUT1" T0
            INNER JOIN "OQUT" T1 ON T0."DocEntry" = T1."DocEntry"
            INNER JOIN "OITM" T2 ON T0."ItemCode" = T2."ItemCode"
            LEFT JOIN "WTR1" T3 ON (T0."ItemCode" = T3."ItemCode" AND T1."DocNum" = T3."U_TI_ORDENVENTA")
        WHERE
        T1."DocNum" = '{docNum}'
        ORDER BY
            T0."ItemCode",
            T0."Dscription";
    """
    return query


def queryGetItemsSaleOrderOrQuotation(
        orderOrQuotation,
        saleOrdersConsulta,
        customerCodeConsulta,
        customerConsulta,
        collectionConsulta,
        descriptionConsulta,
        itemCodeConsulta,
        quantityConsulta,
        stateConsulta,
    ):

    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

    query = f"""

        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            
            DECLARE array_saleOrder INTEGER ARRAY = ARRAY({saleOrdersConsulta});
            DECLARE array_customerCode VARCHAR(25) ARRAY = ARRAY({customerCodeConsulta});
            DECLARE array_customer VARCHAR(80) ARRAY = ARRAY({customerConsulta});
            DECLARE array_collection VARCHAR(40) ARRAY = ARRAY({collectionConsulta});
            DECLARE array_description VARCHAR(20) ARRAY = ARRAY({descriptionConsulta});
            DECLARE array_ItemCode VARCHAR(80) ARRAY = ARRAY({itemCodeConsulta});
            DECLARE array_quantity INTEGER ARRAY = ARRAY({quantityConsulta});
            DECLARE array_state VARCHAR(25) ARRAY = ARRAY({stateConsulta});
            
            DECLARE exist INTEGER;

            LEN:= CARDINALITY(:array_ItemCode);
            CREATE LOCAL TEMPORARY TABLE #AAAB2 ("SaleOr" INTEGER, "doc" varchar(25),"oqt" varchar(80),"docq" varchar(40),"oq" varchar(20),"r" varchar(80), "q" INTEGER, "u" varchar(25));
            
            FOR I IN 1..:LEN DO
            
                INSERT INTO #AAAB2 ("SaleOr","doc", "oqt", "docq","oq", "r", "q", "u") values(:array_saleOrder[I], :array_customerCode[I], :array_customer[I], :array_collection[I], :array_description[I], :array_ItemCode[I], :array_quantity[I], :array_state[I]);
        
            END FOR;
            --select * from #AAAB2;
            SELECT 
                T0."SaleOr",
            	T0."doc",
            	T0."oqt",
            	T0."docq",
            	T0."oq",
            	T0."r",
            	T0."q",
                T2."Quantity",
                (T2."Quantity" -T0."q") as "Pendiente",
                100 - (100/T2."Quantity" *(T2."Quantity" -T0."q")) as "%",
                T0."u"
                
            FROM #AAAB2 T0
            INNER JOIN "{queryDbs[0]}" T1 ON T1."DocNum" =  T0."SaleOr"
            INNER JOIN "{queryDbs[1]}" T2 ON (T1."DocEntry" =  T2."DocEntry" and T0."oq" = T2."ItemCode")
            --where "DocNum" in ('1295')
            order by T0."oqt"
        ;
            DROP TABLE #AAAB2;
        END;  
    """
    # print(query)

    # with open("consulta.txt", "w") as archivo:
    #     archivo.write(query)

    return query


def queryGetItemsSaleQuotationAndOrderImage(docNum, orderOrQuotation):
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

    query = f"""
        SELECT 
            T0."ItemCode", 
            T0."Dscription", 
            T0."Quantity", 
            T2."CodeBars",
            T0."WhsCode",
            --'\\10.238.117.2\ImagesJO\'  || "U_GSP_Picture"
            '\\10.238.117.2\\' || (select "BitmapPath" from OADP) || "U_GSP_Picture"
            ,T0."Price" as "precio"
            ,T0."Currency" as "Moneda"
        FROM 
            "{queryDbs[1]}" T0
            INNER JOIN "{queryDbs[0]}" T1 ON T0."DocEntry" = T1."DocEntry"
            INNER JOIN "OITM" T2 ON T0."ItemCode" = T2."ItemCode"
            LEFT JOIN "WTR1" T3 ON (T0."ItemCode" = T3."ItemCode" AND T1."DocNum" = T3."U_TI_ORDENVENTA")
            LEFT JOIN "@GSP_TCMODEL" T4 ON T2."U_GSP_REFERENCE" = T4."U_GSP_REFERENCE"
        WHERE
        T1."DocNum" = '{docNum}'
        ORDER BY
            T0."ItemCode",
            T0."Dscription";
    """
    # console.log(query)
    return query
    

def queryStatusCustomerByDate(fec_desde, fec_hasta):
    query = """
        SELECT  Q1."CardCode", Q1."CardName", Q1."Quantity", Q1."Valor", Q2."Quantity", Q2."Valor", Q3."Cantidad", Q3."Valor"
            FROM(
                SELECT T1."CardCode", T1."CardName", SUM(T2."Quantity") as "Quantity" , SUM(T2."Price" * T2."Quantity") as "Valor", T2."Currency"
                FROM "ORDR" T1 INNER JOIN "RDR1" T2 ON T2."DocEntry" = T1."DocEntry"
                WHERE T1."TaxDate" between to_date('"""+fec_desde+"""', 'YYYY-MM-DD') AND to_date('"""+fec_hasta+"""', 'YYYY-MM-DD')
                GROUP BY T1."CardCode", T1."CardName", T2."Currency"
        ) Q1

        LEFT JOIN (SELECT T3."CardCode", T3."CardName", SUM(T4."Quantity")as "Quantity" , SUM(T4."Price" * T4."Quantity")  as "Valor", T4."Currency"
            FROM "OINV" T3 INNER JOIN "INV1" T4 ON T4."DocEntry" = T3."DocEntry"
            WHERE LEFT (T3."CardCode",1) LIKE 'C' AND T3."TaxDate" between to_date('"""+fec_desde+"""', 'YYYY-MM-DD') AND to_date('"""+fec_hasta+"""', 'YYYY-MM-DD')
            GROUP BY T3."CardCode", T3."CardName", T4."Currency" 
            ) Q2 
            ON Q1."CardCode" = Q2."CardCode" 

        LEFT JOIN (SELECT T5."CardCode", SUM(T6."Quantity") AS "Cantidad", SUM(T6."Price" * T6."Quantity") as "Valor", T6."Currency"
            FROM "OQUT" T5 INNER JOIN "QUT1" T6 ON T6."DocEntry" = T5."DocEntry"
            LEFT JOIN "OINV" T7 ON T7."U_TI_SALESOFFER" = T5."DocNum"
            WHERE T7."U_TI_SALESOFFER" IS NULL AND T5."TaxDate" between to_date('"""+fec_desde+"""', 'YYYY-MM-DD') AND to_date('"""+fec_hasta+"""', 'YYYY-MM-DD')
            GROUP BY T5."CardCode", T6."Currency"
            ) Q3
            ON Q1."CardCode" = Q3."CardCode" 

        ORDER BY Q1."CardName";
    """
    return query


def queryStatusCustomerByCollection(collection):
    query = """
    SELECT  Q1."CardCode", Q1."CardName", Q1."Quantity", Q1."Valor", Q2."Quantity", Q2."Valor", Q3."Cantidad", Q3."Valor"
        FROM(
            SELECT T1."CardCode", T1."CardName", SUM(T2."Quantity") as "Quantity" , SUM(T2."Price" * T2."Quantity") as "Valor", T2."Currency"
            FROM "ORDR" T1 INNER JOIN "RDR1" T2 ON T2."DocEntry" = T1."DocEntry" INNER JOIN "OITM" T8 ON T8."ItemCode" = T2."ItemCode"
            WHERE T8."U_GSP_Season" = '"""+collection+"""'
            GROUP BY T1."CardCode", T1."CardName", T2."Currency"
    ) Q1
    
    LEFT JOIN (SELECT T3."CardCode", T3."CardName", SUM(T4."Quantity")as "Quantity" , SUM(T4."Price" * T4."Quantity")  as "Valor", T4."Currency"
        FROM "OINV" T3 INNER JOIN "INV1" T4 ON T4."DocEntry" = T3."DocEntry" INNER JOIN "OITM" T9 ON T9."ItemCode" = T4."ItemCode"
        WHERE LEFT (T3."CardCode",1) LIKE 'C' AND T9."U_GSP_Season" = '"""+collection+"""' 
        GROUP BY T3."CardCode", T3."CardName", T4."Currency" 
        ) Q2 
        ON Q1."CardCode" = Q2."CardCode" 
    
    LEFT JOIN (SELECT T5."CardCode", SUM(T6."Quantity") AS "Cantidad", SUM(T6."Price" * T6."Quantity") as "Valor", T6."Currency"
        FROM "OQUT" T5 INNER JOIN "QUT1" T6 ON T6."DocEntry" = T5."DocEntry" INNER JOIN "OITM" T10 ON T10."ItemCode" = T6."ItemCode"
        LEFT JOIN "OINV" T7 ON T7."U_TI_SALESOFFER" = T5."DocNum"
        WHERE T7."U_TI_SALESOFFER" IS NULL AND T10."U_GSP_Season" = '"""+collection+"""' 
        GROUP BY T5."CardCode", T6."Currency"
        ) Q3
        ON Q1."CardCode" = Q3."CardCode" 
    
    ORDER BY Q1."CardName";
    """

    #print(query)
    return query


def queryGetInvoiceReport(fecini, fecfin):
    query = """
        SELECT
            Q1."CardCode",
            Q1."CardName",
            Q1."ItemCode", 
            SUM(Q1."Quantity"), 
            Q1."Price",
            Q1."DocNum",
            Q1."Subpartida1",
            Q1."Subpartida2",
            Q1."Address",
            Q1."TaxDate",
            Q1."Country",
            Q1."City",
            Q1."Moneda",
            Q1."TotalFact",
            Q1."TotalFactDivisa",
            Q1."DescuentoPesos",
            Q1."DescuentoDivisa"
        FROM(
            SELECT
                T1."CardCode",
                T1."CardName",
                T1."DocEntry" AS "DocEntry",
                T1."DocNum" AS "DocNum",
                T1."NumAtCard" AS "NumAtCard",
                T1."Address",
                T1."TaxDate" AS "TaxDate",
                T1."U_TI_TOTALBOXES" AS "U_TI_TOTALBOXES",
                T1."U_TI_GROSSWEIGHT" AS "U_TI_GROSSWEIGHT",
                T1."U_TI_NETWEIGHT" AS "U_TI_NETWEIGHT",
                "SPLIT_WITH_DELIMITER"(T0."ItemCode", '_',1) AS "ItemCode",
                T0."Quantity" AS "Quantity",
                T0."Price" AS "Price",
                T6."Name" AS "Country",
                T4."U_PARDESC" AS "Subpartida1",
                T5."U_TI_PARCODE" AS "Subpartida2",
                T2."City" AS "City",
                T1."DocCur" AS "Moneda",
                T1."DocTotal" AS "TotalFact",
                T1."DocTotalFC" AS "TotalFactDivisa",
                T1."DiscSum" AS "DescuentoPesos",
                T1."DiscSumFC" AS "DescuentoDivisa"
            FROM
                "INV1" T0
                INNER JOIN "OINV" T1 ON T0."DocEntry" = T1."DocEntry"
                INNER JOIN "CRD1" T2 ON T1."CardCode" = T2."CardCode"
                INNER JOIN "OCRD" T3 ON T2."CardCode" = T3."CardCode"
                LEFT JOIN "@TI_COMPOSITION_DOC" T4 ON "SPLIT_WITH_DELIMITER"(T0."ItemCode", '_',1) = T4."U_REFDESC"
                LEFT JOIN "OITM" T5 ON T0."ItemCode" = T5."ItemCode"
                INNER JOIN "OCRY" T6 ON T2."Country" = T6."Code"
            WHERE
                T0."ItemCode" IS NOT NULL
            ORDER BY "ItemCode" ASC
        )Q1
        WHERE
            Q1."TaxDate" BETWEEN to_date('"""+str(fecini)+"""', 'YYYY-MM-DD') AND to_date('"""+str(fecfin)+"""', 'YYYY-MM-DD')
        GROUP BY 
            Q1."ItemCode", 
            Q1."Price",
            Q1."DocEntry",
            Q1."DocNum",
            Q1."Subpartida1",
            Q1."Subpartida2",
            Q1."TaxDate",
            Q1."U_TI_TOTALBOXES",
            Q1."U_TI_GROSSWEIGHT",
            Q1."U_TI_GROSSWEIGHT",
            Q1."U_TI_NETWEIGHT",
            Q1."Country",
            Q1."City",
            Q1."Address",
            Q1."CardName",
            Q1."CardCode",
            Q1."Moneda",
            Q1."TotalFact",
            Q1."TotalFactDivisa",
            Q1."DescuentoPesos",
            Q1."DescuentoDivisa";
    """
    return query


def queryGetInfoReferenceSAPCodebarsSaleOrder(docNum, codebars, orderOrQuotation):
    saleOrderDbs= ("ORDR","RDR1")
    saleQuotationDbs = ("OQUT", "QUT1")
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs
    query = f"""
    SELECT 
        T0."ItemCode",
        T2."ItemName",
        T2."CodeBars",
        T0."Price"
    FROM 
        {queryDbs[1]} T0
        INNER JOIN {queryDbs[0]} T1 ON T0."DocEntry" = T1."DocEntry"
        INNER JOIN "OITM" T2 ON T0."ItemCode" = T2."ItemCode"
    WHERE
        T2."CodeBars" = '"""+str(codebars)+"""'
        AND T1."DocNum" = '"""+str(docNum)+"""';
    """
    return query


def queryGetNumTotalItemsSaleOrder(docNum):

    query = """
    SELECT
        SUM(T0."Quantity")
    FROM
        "RDR1" T0
        INNER JOIN "ORDR" T1 ON T0."DocEntry" = T1."DocEntry"
    WHERE T1."DocNum" = '"""+docNum+"""';
    """

    return query


def queryGetTotalNoItemsCollection(collection):

    saleOrderDbs= ("ORDR","RDR1")
    saleQuotationDbs = ("OQUT", "QUT1")

    listCollections = [
        "001",
        "003",
        "004",
        "005",
        "006",
        "009",
        "011",
        "014",
        "28",
        "025",
        "024",
        "021",
        "020",
    ]

    verify = any(collection == v for v in listCollections)

    if verify:
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

    query = f"""
    SELECT 
        SUM(T0."Quantity")
    FROM
        "{queryDbs[1]}" T0
        INNER JOIN "{queryDbs[0]}" T1 ON T0."DocEntry" = T1."DocEntry"
        INNER JOIN "OITM" T2 ON T0."ItemCode" = T2."ItemCode"
    WHERE
        T2."U_GSP_COLLECTION" = '{collection}';
    """
    return query


def queryGetListInvoicesOfSaleOrder(docNumSaleOrder):
    """
    Consulta de Sap para obtener el numero de factura correspondiente al documento 
    de la orden de venta

    """
    query = f"""
        select T2."DocNum" from ORDR T0
        left JOIN INV1 T1 ON T1."BaseEntry" = T0."DocEntry"
        left join OINV T2 ON T2."DocEntry" = T1."DocEntry"
        where T0."DocNum" = {docNumSaleOrder}
        group by T2."DocNum";

    """
    #console.log(query)
    return query
    
    #Consulta anterior
    """
    SELECT 
        T1."SeriesName",
        T0."DocNum"
    FROM 
        "OINV" T0
        INNER JOIN "NNM1" T1 ON T0."Series" = T1."Series" 
    WHERE
        "U_TI_SALEORDER" = {docNumSaleOrder};
    """
    
def queryGetListInvoicesOfSaleQuotations(docNumSaleOrder):
    """
    Consulta de Sap para obtener el numero de factura correspondiente al documento 
    de la orden de venta

    """
    query = f"""
        SELECT distinct 
            T8."DocNum" as "Numero_de_Factura",
            --T6."DocNum" as "Numero_de_Entrega",
            --T3."DocNum" as "Numero_de_orden_de_venta",
            T0."DocNum" as "Numero_de_oferta_de_venta"
        FROM OQUT T0
            INNER JOIN QUT1 T1 ON T1."DocEntry" = T0."DocEntry"
            INNER JOIN RDR1 T2 ON T2."BaseEntry" = T1."DocEntry" AND T2."BaseLine" = T1."LineNum"
            INNER JOIN ORDR T3 ON T3."DocEntry" = T2."DocEntry"
            INNER JOIN ODLN T6 ON T6."DocEntry" = T2."TrgetEntry"
            INNER JOIN DLN1 T7 on T7."DocEntry" = T6."DocEntry"
            INNER JOIN OINV T8 ON T8."DocEntry" = T7."TrgetEntry"
        WHERE T0."DocNum" =  {docNumSaleOrder};
    """
    #console.log(query)
    return query

def queryGetListAllCollection():
    query = """
    SELECT 
        "Code", 
        "Name" 
    FROM 
        "@GSP_TCCOLLECTION"
    order by "Name";
    """
    return query


# migrado de nombre de coleccion a codigo de coleccion
# def queryGetInfoStatusPickingBilledByCardNameAndCollection(collectionId, cardCode):
#     query = f"""
#         SELECT
#             Q1."CardCode",
#             Q1."Coleccion",
#             SUM(Q1."TotalRecaudo") AS "TotalRecaudo",
#             SUM(Q1."Cantidad") AS "CantidadItems"
#         FROM (
#             SELECT 
#                 (T0."CardCode") AS "CardCode",
#                 (T0."DocNum") AS "DocNum",
#                 MAX(T3."Name") AS "Coleccion",
#                 SUM(T1."Quantity") AS "Cantidad",
#                 (
#                 SELECT 
#                     SUM(A."DocTotalFC")
#                 FROM
#                     "OINV" A
#                     INNER JOIN "NNM1" B ON A."Series" = B."Series"
#                 WHERE
#                     A."U_TI_SALEORDER" = T0."DocNum"
#                 ) AS "TotalRecaudo"
#             FROM
#                 "ORDR" T0
#                 INNER JOIN "RDR1" T1 ON T0."DocEntry" = T1."DocEntry"
#                 INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
#                 INNER JOIN "@GSP_TCCOLLECTION" T3 ON T2."U_GSP_COLLECTION" = T3."Code"
#             WHERE
#                 T3."Code" = '{collectionId}' AND T0."CardCode" = '{cardCode}'
#             GROUP BY
#                 T0."DocNum",
#                 T0."CardCode"
#             ORDER BY
#                 T0."DocNum"
#         )Q1
#         GROUP BY
#             Q1."Coleccion",
#             Q1."CardCode"
#         ORDER BY
#             Q1."CardCode";
#     """

#     return query


def queryGetAllCustomer():
    query = """
        SELECT
            T0."CardCode"
            T0."CardName"
        FROM
            "OCRD" T0
        WHERE
            LEFT (T0."CardCode",2) LIKE 'CE'
            OR LEFT (T0."CardCode",2) LIKE 'CN'
        ORDER BY 
            T0."CardCode";
    """
    return query


# migrado de nombre de coleccion a codigo de coleccion
def queryGetTotalUndSaleOrdersByCustomerCodeAndCollection(customerCode, collectionId, verify):
    saleOrderDbs= ("ORDR","RDR1")
    saleQuotationDbs = ("OQUT", "QUT1")
    if verify:
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs
    query = f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({customerCode});
            DECLARE list_exist INTEGER;

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #temporaryresults ("totalund" FLOAT,  "total" FLOAT);
            FOR I IN 1..:LEN DO
                INSERT INTO #temporaryresults ("totalund", "total")
                
                SELECT
                    SUM(T1."Quantity"),
                    SUM( T0."DocTotalFC") as totalSaleOrder
                FROM
                    "{queryDbs[0]}" T0
                    INNER JOIN "{queryDbs[1]}" T1 ON T0."DocEntry" = T1."DocEntry"
                    INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
                    INNER JOIN "@GSP_TCCOLLECTION" T3 ON T2."U_GSP_COLLECTION" = T3."Code"
                WHERE
                    T0."CardCode" = (:array_vars[I])
                    AND T3."Code" = '{collectionId}';
            END FOR;
            SELECT * FROM #temporaryresults;
            DROP TABLE #temporaryresults;
        END;
    """
    # console.log(query)


    # with open('archivo.txt', 'w') as fichero:
        # Escribir una línea en el fichero
        # fichero.write(query)
    #
    
    return query
    

# migrado de nombre de coleccion a codigo de coleccion
def queryGetSumTotalProforma(customerCode, collectionId):
    query = f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({customerCode});
            DECLARE list_exist INTEGER;

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #temporaryresults ( "sumdoctotalfc" FLOAT);
            FOR I IN 1..:LEN DO
                INSERT INTO #temporaryresults ("sumdoctotalfc")
                SELECT
            SUM(Q1."DocTotalFC")
            FROM (
                SELECT 
                    T0."DocNum",
                    T0."DocTotalFC",
                    T3."Name"
                FROM 
                    "OQUT" T0
                    INNER JOIN "QUT1" T1 ON T0."DocEntry" = T1."DocEntry"
                    INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
                    INNER JOIN "@GSP_TCCOLLECTION" T3 ON T2."U_GSP_COLLECTION" = T3."Code"
                WHERE
                    T0."DocStatus" = 'O'
                    AND T0."CardCode" = (:array_vars[I])
                    AND T3."Code" = '{collectionId}'
                GROUP BY
                    T0."DocNum",
                    T0."DocTotalFC",
                    T3."Name"
            ) Q1;
                    
            END FOR;
            SELECT * FROM #temporaryresults;
            DROP TABLE #temporaryresults;
        END;
    """
    return query


# migrado de nombre de coleccion a codigo de coleccion
def queryGetSumTotalInvoice(customerCode, collectionId):
    query= f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({customerCode});
            DECLARE list_exist INTEGER;

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #temporaryresults ( "sumdoc" FLOAT);
            FOR I IN 1..:LEN DO
                INSERT INTO #temporaryresults ("sumdoc")
                SELECT
                SUM(Q1."DocTotalFC")
                FROM (
                    SELECT 
                        T0."DocNum",
                        T0."DocTotalFC",
                        T3."Name"
                    FROM 
                        "OINV" T0
                        INNER JOIN "INV1" T1 ON T0."DocEntry" = T1."DocEntry"
                        INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
                        INNER JOIN "@GSP_TCCOLLECTION" T3 ON T2."U_GSP_COLLECTION" = T3."Code"
                    WHERE
                        T0."DocStatus" = 'O'
                        AND T0."CardCode" = (:array_vars[I])
                        AND T3."Code" = '{collectionId}'
                    GROUP BY
                        T0."DocNum",
                        T0."DocTotalFC",
                        T3."Name"
                    ) Q1;
                    
            END FOR;
            SELECT * FROM #temporaryresults;
            DROP TABLE #temporaryresults;
        END;
    
    """

    """
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({customerCode});
            DECLARE list_exist INTEGER;

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #temporaryresults ( "sumdoc" FLOAT);
            FOR I IN 1..:LEN DO
                INSERT INTO #temporaryresults ("sumdoc")
                SELECT
                SUM(Q1."DocTotalFC")
                FROM (
                    SELECT 
                        T0."DocNum",
                        T0."DocTotalFC",
                        T3."Name"
                    FROM 
                        "OINV" T0
                        INNER JOIN "INV1" T1 ON T0."DocEntry" = T1."DocEntry"
                        INNER JOIN "OITM" T2 ON T1."ItemCode" = T2."ItemCode"
                        INNER JOIN "@GSP_TCCOLLECTION" T3 ON T2."U_GSP_COLLECTION" = T3."Code"
                    WHERE
                        T0."DocStatus" = 'O'
                        AND T0."CardCode" = (:array_vars[I])
                        AND T3."Name" = '{collectionName}'
                    GROUP BY
                        T0."DocNum",
                        T0."DocTotalFC",
                        T3."Name"
                    ) Q1;
                    
            END FOR;
            SELECT * FROM #temporaryresults;
            DROP TABLE #temporaryresults;
        END;
    
    """
    return query


def queryGetCountryOrigin(references):
    query= f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({references});
            DECLARE exist INTEGER;

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #AAAB2 ("U_TI_PAIORI" INTEGER);
            
            FOR I IN 1..:LEN DO
                SELECT  count("U_TI_PAIORI") into exist
                From "@TI_COMPOSITION_DOC"
                WHERE U_REFDESC = (:array_vars[I]);
                
                    IF (:exist = 0) then
                        INSERT INTO #AAAB2 ("U_TI_PAIORI") VALUES (1);
                    ELSE	
                        INSERT INTO #AAAB2 ("U_TI_PAIORI")
                            SELECT  "U_TI_PAIORI"
                            From "@TI_COMPOSITION_DOC"
                            WHERE U_REFDESC = (:array_vars[I]);
                    END IF; 
            END FOR;
            SELECT * FROM #AAAB2 ;
            DROP TABLE #AAAB2;
        END;
    """
    # console.log(query)
    return query


def queryGetUnitMeasure(references):
    query= f"""
        DO
        BEGIN
        DECLARE I INTEGER;                                                                         
        DECLARE LEN INTEGER;                                                                       
        DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({references});                                 
        DECLARE exist INTEGER;                                                                     
                                                                                                    
        LEN:= CARDINALITY(:array_vars);                                                            
        CREATE LOCAL TEMPORARY TABLE #AAAB2 ("UnitMsr" VARCHAR(20), "Subpartida" VARCHAR(20));                               
                                                                                                    
        FOR I IN 1..:LEN DO                                                                        
            /*SELECT "SalUnitMsr" into exist                                                
            From "OITM"                                                             
            WHERE "ItemCode" = (:array_vars[I]);                                                    
            */                                                                                       
                /*IF (:exist = 0) then                                                               
                    INSERT INTO #AAAB2 ("UnitMsr") VALUES (1);                                 
                ELSE
                */                                                                               
            INSERT INTO #AAAB2 ("UnitMsr", "Subpartida")                                             
                SELECT "SalUnitMsr",                                              
                    T1."U_PARDESC"                                                                                                                                     
                From "OITM" T0
                LEFT JOIN "@TI_COMPOSITION_DOC" T1 ON T1."U_REFDESC" = T0."U_GSP_REFERENCE"                                                    
                WHERE "ItemCode" = (:array_vars[I]);                                        
                --END IF;                                                                            
        END FOR;                                                                                   
        SELECT * FROM #AAAB2 ;                                                                     
        DROP TABLE #AAAB2;   
        END;
    """

    console.log(query)
    return query


# def queryGetSaleOrderCollection(orderPV, orderOrQuotation):
#     saleOrderDbs= ("ORDR","RDR1")
#     saleQuotationDbs = ("OQUT", "QUT1")
#     if orderOrQuotation == "order":
#         queryDbs = saleOrderDbs
#     else:
#         queryDbs = saleQuotationDbs
#     query = f"""
#         SELECT  MAX(C."Name") 
#         FROM 
#             {queryDbs[1]} A
#             INNER JOIN "OITM" B ON A."ItemCode" = B."ItemCode"
#             INNER JOIN "@GSP_TCCOLLECTION" C ON B."U_GSP_COLLECTION" = C."Code"
#             INNER JOIN {queryDbs[0]} D ON A."DocEntry" = D."DocEntry"
#         WHERE D."DocNum" = '{orderPV}'
#     """
#     return query


def queryGetSaleOrderCollectionId(orderPV, orderOrQuotation):
    saleOrderDbs= ("ORDR","RDR1")
    saleQuotationDbs = ("OQUT", "QUT1")
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

        
    query = f"""
        SELECT DISTINCT C."Code"
        FROM 
            {queryDbs[1]} A
            INNER JOIN "OITM" B ON A."ItemCode" = B."ItemCode"
            INNER JOIN "@GSP_TCCOLLECTION" C ON B."U_GSP_COLLECTION" = C."Code"
            INNER JOIN {queryDbs[0]} D ON A."DocEntry" = D."DocEntry"
        WHERE D."DocNum" = '{orderPV}'
    """
    # console.log(query)
    return query


def queryGetCollectionIDByName(collectionName):
    query = f"""
        select "Code"
        from "@GSP_TCCOLLECTION" C
        where C."Name" = '{collectionName}'
        order by "Code"
    """
    return query


def dropTemporaryColumn():
    query="""
        DO
        BEGIN
        DECLARE list_exist INTEGER;
        SELECT COUNT(*) INTO list_exist FROM PUBLIC.M_TABLES WHERE schema_name = 'SBOPRUEBASJOCOL' AND table_name = 'AAB1';

        IF (:list_exist > 0) THEN
            DROP TABLE SBOPRUEBASJOCOL.AAB1;
        END IF;

        END;   
    """
    return query



def queryGetWarehouses():
    query =  f"""
        select 
            "WhsCode"
        from OWHS
        order by "WhsCode"
    """
    return query

def queryGetSingleItemName(itemCode):
    query = f"""
        select "ItemName" from OITM
        where "ItemCode" = '{itemCode}';
    """ 
    return query


def queryGetSingleItemNameByBarCode(itemCode):
    query = f"""
        select "ItemName", "ItemCode" from OITM
        where "CodeBars" = '{itemCode}';
    """
    return query



def queryGetMultipleItemName(itemCodes):
    query = f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({itemCodes});
            DECLARE exist INTEGER;

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #ITEMTABLE ("Name" VARCHAR(120));
            
            FOR I IN 1..:LEN DO
                select count("ItemName") into exist from OITM
                where "ItemCode" = (:array_vars[I]);
                
                    IF (:exist = 0) then
                        INSERT INTO #ITEMTABLE ("Name") VALUES (0);
                    ELSE	
                        INSERT INTO #ITEMTABLE ("Name")
                            SELECT  "ItemName"
                            From OITM
                            WHERE "ItemCode" = (:array_vars[I]);
                    END IF; 
            END FOR;
            SELECT * FROM #ITEMTABLE ;
            DROP TABLE #ITEMTABLE;
        END;
    """
    return query


def queryGetInventoryConsolidationReport(itemCodes, quantities, warehouse):
    query = f"""
    DO
    BEGIN
        DECLARE I INTEGER;
        DECLARE LEN INTEGER;
        DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({itemCodes});
        DECLARE array_quantity VARCHAR(20) ARRAY = ARRAY({quantities});

        LEN:= CARDINALITY(:array_vars);
        CREATE LOCAL TEMPORARY TABLE #AAAB2 ("Referencia" VARCHAR(20), "TomaFisica" DOUBLE, "cantidadSAP" DOUBLE, "Resta" DOUBLE);
        
        FOR I IN 1..:LEN DO

            INSERT INTO #AAAB2 ("Referencia", "TomaFisica", "cantidadSAP", "Resta")
            values(:array_vars[I], :array_quantity[I], 0, 0);

        END FOR;
        SELECT T1."ItemCode" as "Codigo Sap",
            T2."ItemName" as "Referencia",
            COALESCE(T0."TomaFisica", 0) as "TomaFisica",
            T1."OnHand" as "cantidadSAP", 
            COALESCE(T0."TomaFisica" - T1."OnHand", 0)  as "Resta"
            --"WhsCode" as "Bodega"
        FROM #AAAB2 T0 
        right join OITW T1 on T0."Referencia" = T1."ItemCode"
        inner join OITM T2 on T2."ItemCode" = T1."ItemCode"
        where
            "WhsCode" = '{warehouse}';
        DROP TABLE #AAAB2;
    END;
    """
    
    """
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({itemCodes});
            DECLARE array_quantity VARCHAR(20) ARRAY = ARRAY({quantities});

            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #AAAB2 ("Referencia" VARCHAR(20), "TomaFisica" DOUBLE, "cantidadSAP" DOUBLE, "Resta" DOUBLE);
            
            FOR I IN 1..:LEN DO

                INSERT INTO #AAAB2 ("Referencia", "TomaFisica", "cantidadSAP", "Resta")
                    select "ItemCode",
                    	(:array_quantity[I]) as "TomaF",
                    	"OnHand" as "cantidad",
                    	((:array_quantity[I]) - "OnHand") as "diferencia"
                    from OITW
					where 
					"OnHand" <> 0
					and 
					"WhsCode" = '{warehouse}'
					and 
					"ItemCode" = (:array_vars[I]);	
            END FOR;
            SELECT * FROM #AAAB2 ;
            DROP TABLE #AAAB2;
        END;
        """
        
    # console.log(query)
    return query


def queryGetCustomerData():
    query = """
        select 
            T0."CardCode"
        from  OCRD T0 

        WHERE
            LEFT (T0."CardCode", 2) LIKE 'CE'
            AND T0."GroupCode" in (110) -- Grupo Wholesale
        order by "CardName";
    """

    return query



def queryGetStatusByseveralPickings(textOrders, orderOrQuotation, items, order, quantities, estadosPicking, pesoBruto, pesoNeto, dimensiones):
    
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs
    
    query= f"""
        DO BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({items});
            DECLARE array_quantity INTEGER ARRAY = ARRAY({quantities});
            DECLARE array_orders INTEGER ARRAY = ARRAY({order});
            DECLARE array_pickingStatuses VARCHAR(3) ARRAY = ARRAY({estadosPicking});
            DECLARE array_pesoBruto FLOAT ARRAY = ARRAY({pesoBruto});
            DECLARE array_pesoNeto FLOAT ARRAY = ARRAY({pesoNeto});
            DECLARE array_dimensiones VARCHAR(20) ARRAY = ARRAY({dimensiones});            
                
            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #AAAB2 ("saleOrder" integer, "itemCode" VARCHAR(20) , "quantity" integer, "pickingStatus" VARCHAR(20), "pesoBruto" FLOAT, "pesoNeto" FLOAT, "dimensiones" VARCHAR(20) );
            FOR I IN 1..:LEN DO
                INSERT INTO #AAAB2 ("itemCode", "quantity", "saleOrder", "pickingStatus", "pesoBruto", "pesoNeto", "dimensiones")
                    values(:array_vars[I], :array_quantity[I], :array_orders[I], :array_pickingStatuses[I], :array_pesoBruto[I], :array_pesoNeto[I], :array_dimensiones[I]);             
            END FOR;
            SELECT 
                --T2."itemCode" ,
                T0."DocNum" as "ofertaVenta"
                ,T0."CardName" as "cliente"
                ,T1."ItemCode" as "ItemCode"
                ,T1."Dscription" as "descripcionItem"            
                ,T1."Quantity" as "cantidadSolicitadaSap"
                ,T1."Price" as "precioUnitario"
                ,IFNULL(T2."quantity", 0) as "cantidadEmpacadaWms"
                ,IFNULL(T2."quantity", 0) * T1."Price" as "precioCantidadEmpacadaWms"
                ,T1."Quantity" - IFNULL(T2."quantity", 0) as "saldoPorEnviar"
                ,T1."Quantity" * T1."Price" - IFNULL(T2."quantity", 0) * T1."Price" as "precioSaldoPorEnviar"
                ,IFNULL(T2."pickingStatus", 'sin empacar') as "estadoPciking"
                ,IFNULL(T2."quantity", 0) / T1."Quantity" * 100  as "porcentajeEmpacado"
                ,T1."WhsCode" as "bodega"
                ,T1."Quantity" * T1."Price" as "precioTotal"
                ,T1."Currency" as "moneda"
                ,T2."pesoBruto"
                ,T2."pesoNeto"
                ,T2."dimensiones"
                ,CASE 
                    WHEN T4."U_GSP_Picture" IS NOT NULL OR T4."U_GSP_Picture" <> '' THEN  CONCAT( 'https://johannaortiz.net/media/ImagesJOServer/', REPLACE(T4."U_GSP_Picture", ' ', '%20') ) 
                    ELSE 'La Imagen no ha sido cargada en SAP' 
                END AS "picture"
                ,T4."U_GSP_Picture" as "picturePath"
            FROM "{queryDbs[0]}" T0
            INNER JOIN "{queryDbs[1]}" T1 ON T0."DocEntry" = T1."DocEntry"
            LEFT JOIN #AAAB2 T2 ON T0."DocNum" = T2."saleOrder" AND T1."ItemCode" = T2."itemCode"
            INNER JOIN "OITM" T3 ON T3."ItemCode" = T1."ItemCode"
            LEFT JOIN "@GSP_TCMODEL" T4 ON T4."Code" = T3."U_GSP_ModelCode"
            where
                    T0."DocNum" in ({textOrders})
                ;
            DROP TABLE #AAAB2;
        END;
    """
    
    
    # with open("consulta.sql", "w") as archivo:
    #     archivo.write(query)
    return query



def queryGetStatusByseveralCollectionOrders(textOrders, orderOrQuotation, items, order, quantities, estadosPicking):
    
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs
    
    query= f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({items});
            DECLARE array_quantity INTEGER ARRAY = ARRAY({quantities});
            DECLARE array_orders INTEGER ARRAY = ARRAY({order});
            DECLARE array_pickingStatuses VARCHAR(3) ARRAY = ARRAY({estadosPicking});
            
                
            LEN:= CARDINALITY(:array_vars);
            CREATE LOCAL TEMPORARY TABLE #AAAB2 ("saleOrder" integer, "itemCode" VARCHAR(20) , "quantity" integer, "pickingStatus" VARCHAR(20));

            FOR I IN 1..:LEN DO

                INSERT INTO #AAAB2 ("itemCode", "quantity", "saleOrder", "pickingStatus")
                    values(:array_vars[I], :array_quantity[I], :array_orders[I], :array_pickingStatuses[I]);
                    
                    

            END FOR;

            SELECT 
                --T2."itemCode" ,
                T0."DocNum" as "ofertaVenta"
                ,T0."CardName" as "cliente"
                ,T1."ItemCode" as "ItemCode"
                ,T1."Dscription" as "descripcionItem"
                ,T6."Name" as "coleccionItem"
                ,T1."Quantity" as "cantidadSolicitadaSap"
                ,T1."Price" as "precioUnitario"
                ,IFNULL(T2."quantity", 0) as "cantidadEmpacadaWms"
                ,IFNULL(T2."quantity", 0) * T1."Price" as "precioCantidadEmpacadaWms"
                ,T1."Quantity" - IFNULL(T2."quantity", 0) as "saldoPorEnviar"
                ,T1."Quantity" * T1."Price" - IFNULL(T2."quantity", 0) * T1."Price" as "precioSaldoPorEnviar"
                ,IFNULL(T2."pickingStatus", 'sin empacar') as "estadoPciking"
                ,IFNULL(T2."quantity", 0) / T1."Quantity" * 100  as "porcentajeEmpacado"
                ,T1."WhsCode" as "bodega"
                ,T1."Quantity" * T1."Price" as "precioTotal"
                ,T1."Currency" as "moneda"
                    --,*

            FROM "{queryDbs[0]}" T0
            INNER JOIN "{queryDbs[1]}" T1 ON T0."DocEntry" = T1."DocEntry"
            LEFT JOIN #AAAB2 T2 ON T0."DocNum" = T2."saleOrder" AND T1."ItemCode" = T2."itemCode"
            INNER JOIN "OITM" T3 ON T3."ItemCode" = T1."ItemCode"
            LEFT JOIN "@GSP_TCCOLLECTION" T6 ON T3."U_GSP_COLLECTION" = T6."Code"

            where
                    T0."DocNum" in ({textOrders})
                ;
            DROP TABLE #AAAB2;
        END;
    """

    # console.log(query)

    # with open("./consultaHana.sql", "w") as archivo:
    #     archivo.write(query)

    return query

def querydropSapContingencyTableRegisters():
    query = f"""
        DROP TABLE AAAB2;
        """
    return query


def queryCreateSapContingencyTableRegisters():
    query = f"""
        CREATE TABLE \"AAAB2\" (
                "pickingStatus" VARCHAR(3), 
                "ordenes" INTEGER,
                "items" VARCHAR(20),
                "codigosBarras" VARCHAR(20),
                "codigosBarrasCajas" VARCHAR(25),
                "cantidades" INTEGER,
                "fechas" VARCHAR(30),
                "tipoCajas" VARCHAR(30),
                "Dimensiones" VARCHAR(20),
                "identificadoresDespacho" VARCHAR(20),
                "pesoBruto" FLOAT,
                "pesoNeto" FLOAT,
                "paisOrigen" VARCHAR(20),
                "coleccion" VARCHAR(25),
                "descripcion" VARCHAR(100),
                "talla" VARCHAR(6),
                "color" VARCHAR(6),
                "cliente" VARCHAR(60),
                "responsable" VARCHAR(60)
            );
        """
    return query


def queryInsertSapContingencyTableRegisters(
    pickingStatus,
    ordenes,
    items,
    codigosBarras,
    codigosBarrasCajas,
    cantidades,
    fechas,
    tipoCajas,
    Dimensiones,
    identificadoresDespacho,
    pesoBruto,
    pesoNeto,
    paisOrigen,
    coleccion,
    descripcion,
    talla,
    color,
    cliente,
    responsable,
    ordenesTotales,
):
    query = f"""
        DO
        BEGIN
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;

            DECLARE array_pickingStatuses VARCHAR(3) ARRAY = ARRAY({pickingStatus});
            DECLARE array_orders INTEGER ARRAY = ARRAY({ordenes});
            DECLARE array_items VARCHAR(20) ARRAY = ARRAY({items});
            DECLARE array_barCodes VARCHAR(20) ARRAY = ARRAY({codigosBarras});
            DECLARE array_boxexBarCodes VARCHAR(25) ARRAY = ARRAY({codigosBarrasCajas});
            DECLARE array_quantity INTEGER ARRAY = ARRAY({cantidades});
            DECLARE array_fechas VARCHAR(30) ARRAY = ARRAY({fechas});
            DECLARE array_boxesKinds VARCHAR(30) ARRAY = ARRAY({tipoCajas});
            DECLARE array_dimensions VARCHAR(20) ARRAY = ARRAY({Dimensiones});
            DECLARE array_identifiersDispatch VARCHAR(20) ARRAY = ARRAY({identificadoresDespacho});
            DECLARE array_grossWeight FLOAT ARRAY = ARRAY({pesoBruto});
            DECLARE array_netWeight FLOAT ARRAY = ARRAY({pesoNeto});
            DECLARE array_originCountry VARCHAR(20) ARRAY = ARRAY({paisOrigen});
            DECLARE array_collection VARCHAR(25) ARRAY = ARRAY({coleccion});
            DECLARE array_description VARCHAR(100) ARRAY = ARRAY({descripcion});
            DECLARE array_size VARCHAR(6) ARRAY = ARRAY({talla});
            DECLARE array_color VARCHAR(6) ARRAY = ARRAY({color});
            DECLARE array_customer VARCHAR(60) ARRAY = ARRAY({cliente});
            DECLARE array_responsible VARCHAR(60) ARRAY = ARRAY({responsable});
            
                
            LEN:= CARDINALITY(:array_items);

            FOR I IN 1..:LEN DO

                INSERT INTO AAAB2 (
                    "pickingStatus",
                    "ordenes",
                    "items",
                    "codigosBarras",
                    "codigosBarrasCajas",
                    "cantidades",
                    "fechas",
                    "tipoCajas",
                    "Dimensiones",
                    "identificadoresDespacho",
                    "pesoBruto",
                    "pesoNeto",
                    "paisOrigen",
                    "coleccion",
                    "descripcion",
                    "talla",
                    "color",
                    "cliente",
                    "responsable"
                )
                values(
                    :array_pickingStatuses[I],
                    :array_orders[I],
                    :array_items[I],
                    :array_barCodes[I],
                    :array_boxexBarCodes[I],
                    :array_quantity[I],
                    :array_fechas[I],
                    :array_boxesKinds[I],
                    :array_dimensions[I],
                    :array_identifiersDispatch[I],
                    :array_grossWeight[I],
                    :array_netWeight[I],
                    :array_originCountry[I],
                    :array_collection[I],
                    :array_description[I],
                    :array_size[I],
                    :array_color[I],
                    :array_customer[I],
                    :array_responsible[I]

                );
                    
            END FOR;
        END;
    
    """


    # with open("./consultaHana.sql", "w", encoding="utf-8") as archivo:
    #     archivo.write(query)

    return query



def queryGetContingencyReportVsSapOrder(ordenesTotales,):
    query = f"""
            SELECT  
                IFNULL(T2."pickingStatus", 'sin empacar') as "estadoPicking",
                T0."DocNum" as "orden",
                T1."ItemCode",
                IFNULL(T1."CodeBars", T2."codigosBarras") as "CodigoBarras", 
                T2."codigosBarrasCajas" as "CodigoBarrasCajas",
                IFNULL(T2."cantidades",0) as "Cantidad",
                T1."Quantity" as "CantidadPedido",
                T2."fechas",
                T2."tipoCajas",
                T2."Dimensiones",
                T2."identificadoresDespacho",
                IFNULL(T2."pesoBruto", 0) as "pesoBruto",
                IFNULL(T2."pesoNeto",0) as "pesoNeto",
                T2."paisOrigen",
                T6."Name" as "coleccion", --T2."coleccion",
                T1."Dscription" as "descripcion", --T2."descripcion",
				SUBSTR_REGEXPR( '(?<=_)[^_]*' IN T1."ItemCode" OCCURRENCE 1) as "talla",  --T2."talla",
				SUBSTR_REGEXPR( '(?<=_)[^_]*' IN T1."ItemCode" OCCURRENCE 2) as "color",  --T2."color",
                T0."CardCode" as "codigoCliente", 
                T0."CardName" as "Cliente", --T2."cliente",
                IFNULL(T2."responsable", 'sin asignar') as "responsable"
            FROM "OQUT" T0
		    INNER JOIN "QUT1" T1 ON T0."DocEntry" = T1."DocEntry"
		    INNER JOIN "OITM" T3 ON T3."ItemCode" = T1."ItemCode"
		    --LEFT JOIN "@GSP_TCMODEL" T4 ON T4."U_GSP_REFERENCE" = T3."U_GSP_REFERENCE"
		    --LEFT JOIN "@GSP_TCCOLOR" T5 ON T3."U_GSP_Color" = T5."Code"
		    LEFT JOIN "@GSP_TCCOLLECTION" T6 ON T3."U_GSP_COLLECTION" = T6."Code" --J."U_GSP_COLLECTION" = P."Code"
			--LEFT JOIN "@GSP_TCSIZE" T7 ON T3."U_GSP_Size" = T7."Name"
		    
		    LEFT JOIN AAAB2 T2 ON T0."DocNum" = T2."ordenes" AND T1."ItemCode" = T2."items"
            where T0."DocNum" in ({ordenesTotales})
            order by T0."CardName", T0."DocNum";
    """

    # with open("./consultaHana.sql", "w", encoding="utf-8") as archivo:
    #     archivo.write(query)

    # console.log(query)
    return query



def queryGetOrdersOrQuotationsWithItemsOfCollection(collection, orderOrQuotation, excluirOfertasCanceladas):
    
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

    canceled_filter = 'and (T0."CANCELED" <> \'Y\')' if excluirOfertasCanceladas != 'null' else ''
    
    query = f"""
        SELECT DISTINCT T0."DocNum"
        FROM "{queryDbs[0]}" T0
        INNER JOIN "{queryDbs[1]}" T1 ON T1."DocEntry" = T0."DocEntry"
        INNER JOIN "OITM" T2 ON T2."ItemCode" = T1."ItemCode"
        WHERE T2."U_GSP_COLLECTION" = '{collection}'
        {canceled_filter}  
        ORDER BY "DocNum";
    """
    # console.log(query)
    return query


def queryGetSaleOrderOrQuotationInformation(originOrder, pvOrder, orderOrQuotation, itemCodes, quantities):
    
    if orderOrQuotation == "order":
        queryDbs = saleOrderDbs
    else:
        queryDbs = saleQuotationDbs

        
    query = f"""

         DO
        BEGIN
            
            DECLARE I INTEGER;
            DECLARE LEN INTEGER;
            DECLARE array_vars VARCHAR(20) ARRAY = ARRAY({itemCodes});
            DECLARE quantities INTEGER ARRAY = ARRAY({quantities});

       LEN:= CARDINALITY(:array_vars);
        --DROP TABLE #itemsCompare;
       CREATE LOCAL TEMPORARY TABLE #itemsCompare ("itemCode" VARCHAR(20), "quantity" INTEGER, "originOrder" INTEGER);

       FOR I IN 1..:LEN DO

           INSERT INTO #itemsCompare ("itemCode", "quantity", "originOrder")
               values(:array_vars[I], :quantities[I], {originOrder});
                    
                    

            END FOR;

            SELECT 

                T0."DocNum" as "pvOrder"
                ,T2."originOrder"
                ,T1."ItemCode" as "ItemCode"
                ,T1."Dscription"
                ,T2."itemCode"
                ,T2."quantity" as "packedQuantities"
                ,T1."Quantity" as "totalQuantities"

                --T2."itemCode" ,
                
                --,*

            FROM "{queryDbs[0]}" T0
            INNER JOIN "{queryDbs[1]}" T1 ON T0."DocEntry" = T1."DocEntry"
            LEFT JOIN #itemsCompare T2 ON T1."ItemCode" = T2."itemCode"


            where
                    T0."DocNum" in ({pvOrder})
                ;
            DROP TABLE #itemsCompare;
        END;

    """

    # console.log(query)
    
    return query