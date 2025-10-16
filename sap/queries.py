def queryGetCollections():
    query = '''
        SELECT "U_GSP_SEASON", "Name"
        FROM SBOJOZF."@GSP_TCCOLLECTION"
        WHERE
            "Name" LIKE '%SPRING SUMMER%' OR
            "Name" LIKE '%WINTER SUN%' OR
            "Name" LIKE '%RESORT%' OR
            "Name" LIKE '%SUMMER VACATION%' OR
            "Name" LIKE '%PREFALL%' OR
            "Name" LIKE '%FALL WINTER%'
        ORDER BY "U_GSP_SEASON" DESC;
    '''
    return query

def queryInsertCollection():
    return '''
        INSERT INTO SBOJOZF."@GSP_TCCOLLECTION" ("Code", "Name", "U_GSP_SEASON")
        VALUES (?, ?, ?)
    '''

def queryGetTraceability():
    return '''
        SELECT 
            t1."U_GSP_REFERENCE",
            t2."Name" as "PhaseName",
            t3."Name" as "CollectionName"
        FROM "SBOJOZF"."@GSP_TCMODEL" T1
        INNER JOIN "SBOJOZF"."@GSP_TCSCHEMA" t2 ON t1."U_GSP_Schema" = t2."Code"
        INNER JOIN "SBOJOZF"."@GSP_TCCOLLECTION" t3 ON t1."U_GSP_COLLECTION" = t3."Code"
        WHERE t1."Code" = ? 
    '''

def queryUpdateTraceability():
    return '''
        UPDATE "SBOJOZF"."@GSP_TCMODEL"
        SET "U_GSP_Schema" = ?
        WHERE "Code" = ?
    '''

def queryGetCurrentTraceability():
    return '''
        SELECT TOP 1
            t1."U_GSP_REFERENCE",
            t2."Name" as "PhaseName"
        FROM "SBOJOZF"."@GSP_TCMODEL" T1
        INNER JOIN "SBOJOZF"."@GSP_TCSCHEMA" t2 ON t1."U_GSP_Schema" = t2."Code"
        WHERE t1."Code" = ? 
        ORDER BY t2."Code" DESC
    '''

def queryGetPhaseByCode():
    return '''
        SELECT "Code", "Name"
        FROM "SBOJOZF"."@GSP_TCSCHEMA"
        WHERE "Code" = ?
    '''

def queryGetAllPhases():
    return '''
        SELECT "Code", "Name"
        FROM "SBOJOZF"."@GSP_TCSCHEMA"
        ORDER BY "Code"
    '''

def queryInsertReference():
    return '''
        INSERT INTO "SBOJOZF"."@GSP_TCMODEL" ("U_GSP_REFERENCE", "U_GSP_COLLECTION", "U_GSP_Desc")
        VALUES (?, ?, ?)
    '''

def queryGetReferenceDetail():
    return '''
        SELECT 
            t1."U_GSP_REFERENCE", 
            t1."U_GSP_Picture",
            t1."U_GSP_Desc", 
            t2."Name" as "SchemaName",
            t3."Name" as "CollectionName"
        FROM "SBOJOZF"."@GSP_TCMODEL" T1
        INNER JOIN "SBOJOZF"."@GSP_TCSCHEMA" t2 ON t1."U_GSP_Schema" = t2."Code"
        INNER JOIN "SBOJOZF"."@GSP_TCCOLLECTION" t3 ON t1."U_GSP_COLLECTION" = t3."Code"
        WHERE t1."U_GSP_REFERENCE" = ?
    '''

def querySearchReference():
    return '''
        SELECT 
            t1."U_GSP_REFERENCE", 
            t1."U_GSP_Picture",
            t1."U_GSP_Desc", 
            t3."Name" as "CollectionName"
        FROM "SBOJOZF"."@GSP_TCMODEL" T1
        INNER JOIN "SBOJOZF"."@GSP_TCCOLLECTION" t3 ON t1."U_GSP_COLLECTION" = t3."Code"
        WHERE t1."U_GSP_REFERENCE" LIKE ? OR t1."U_GSP_Desc" LIKE ?
    '''

def queryGetReferencesByYear():
    return '''
        SELECT 
        t1."U_GSP_REFERENCE", 
        t1."U_GSP_Picture",
        t1."U_GSP_Desc", 
        t2."Name"   
        FROM "SBOJOZF"."@GSP_TCMODEL" T1
        INNER JOIN "SBOJOZF"."@GSP_TCSCHEMA" t2 ON t1."U_GSP_Schema" = t2."Code"
        WHERE t1.U_GSP_COLLECTION = ?
        AND LEFT(t1.U_GSP_REFERENCE, 2) IN ('PT')
        ORDER BY t1.U_GSP_REFERENCE DESC
    '''

def queryTelasPorReferencia():
    query = '''
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
        WHERE T1."U_GSP_REFERENCE" = ?
            AND T1."U_GSP_COLLECTION" = ?
            AND LEFT (T2."U_GSP_ItemCode", 3) IN ('TEN','TE0')
        ORDER BY "U_GSP_SchLinName" DESC;'''
    return query


def queryInsumosPorReferencia():
    query = '''
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
        WHERE T1."U_GSP_REFERENCE" = ?
            AND T1."U_GSP_COLLECTION" = ?
            AND LEFT (T2."U_GSP_ItemCode", 3) IN ('INN','IN0')
        ORDER BY "U_GSP_SchLinName" DESC;'''
    return query
