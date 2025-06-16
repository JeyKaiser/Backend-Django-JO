SET SCHEMA
    "SBOJOZF";

SELECT
    CASE
        WHEN LEFT (H."ItemCode", 1) LIKE 'S' THEN (
            SELECT
                REPLACE(
                    REPLACE(
                        IFNULL(A."U_Ti_CODEDESCINITIAL", '') || ' ' || IFNULL(TO_DECIMAL(A."U_TI_PORCENTCOMP1", 3, 2), 0) || '% ' || IFNULL(A."U_TI_COMPCODE1", '') || ' ' || IFNULL(TO_DECIMAL(A."U_TI_PORCENTCOMP2", 3, 2), 0) || '% ' || IFNULL(A."U_TI_COMPCODE2", '') || ' ' || IFNULL(TO_DECIMAL(A."U_TI_PORCENTCOMP3", 3, 2), 0) || '% ' || IFNULL(A."U_TI_COMPCODE3", '') || ' ' || IFNULL(TO_DECIMAL(A."U_TI_PORCENTCOMP4", 3, 2), 0) || '% ' || IFNULL(A."U_TI_COMPCODE4", '') || ' ' || IFNULL(TO_DECIMAL(A."U_TI_PORCENTCOMP5", 3, 2), 0) || '% ' || IFNULL(A."U_TI_COMPCODE5", '') || ' ' || IFNULL(TO_DECIMAL(A."U_TI_PORCENTCOMP6", 3, 2), 0) || '% ' || IFNULL(A."U_TI_COMPCODE6", '') || ' ' || IFNULL(A."U_TI_CODDESCEND", ''),
                        ' 0.00%',
                        ''
                    ),
                    '  ',
                    ''
                ) AS "REF_SALINI"
            FROM
                "OITM" A
            WHERE
                A."ItemCode" = H."ItemCode"
        )
        ELSE (
            SELECT
                REPLACE(
                    REPLACE(
                        IFNULL(T24."U_DESCINITDESC", '') || ' ' || IFNULL(T24."U_COMPDESC1", '') || ' ' || IFNULL(T24."U_COMPCODE1", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP1", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC2", '') || ' ' || IFNULL(T24."U_COMPCODE2", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP2", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC3", '') || ' ' || IFNULL(T24."U_COMPCODE3", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP3", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC4", '') || ' ' || IFNULL(T24."U_COMPCODE4", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP4", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC5", '') || ' ' || IFNULL(T24."U_COMPCODE5", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP5", 3, 2), 0) || '% ' || IFNULL(T24."U_COMPDESC6", '') || ' ' || IFNULL(T24."U_COMPCODE6", '') || ' ' || IFNULL(TO_DECIMAL(T24."U_PORCENTCOMP6", 3, 2), 0) || '% ' || IFNULL(T24."U_DESCENDDESC", ''),
                        ' 0.00%',
                        ''
                    ),
                    '  ',
                    ''
                ) AS "REF_PT"
            FROM
                "@TI_COMPOSITION_DOC" T24
            WHERE
                T24."U_REFDESC" = "SPLIT_WITH_DELIMITER"(H."ItemCode", '_', 1)
        )
    END AS "Composicion",
    Q."Name" AS "Tipo Tejido",
    A."U_TI_PAIORI" AS "Pais Origen",
    R."Name" AS "Nombre Comercial",
    (
        SELECT
            "BitmapPath"
        FROM
            "OADP"
    ) ||(
        J."" H."ItemCode" AS "COD_ARTICULO",
        A."ItemName" AS "DESCRIPCION",
        A."CardCode" AS "CODIGO_SOCIO",
        B."CardName" AS "Desc proveedor",
        C."Name" AS "Color",
        H."OnHand" AS "STOCK",
        A."BWidth1" AS "ANCHO",
        D."Name" AS "TALLA",
        A."U_TI_CODESIIGO",
        A."SuppCatNum" AS "NUM_CATALOGO",
        F."AvgPrice" AS "PRECIO_ARTICULO",
        F."AvgPrice" * H."OnHand" AS "TOTAL",
        H."WhsCode" AS "ALM ",
        I."WhsName" AS "NAMEALM",
        CASE
            WHEN LEFT (A."ItemCode", 1) LIKE 'S' THEN (
                SELECT
                    T1."U_GSP_Season"
                FROM
                    "OITM" T1
                WHERE
                    T1."ItemCode" = A."ItemCode"
            )
            ELSE (G."Name")
        END AS Temporada,
        K."Name" AS "LINEA",
        M."Name" AS "SUBLINEA",
        (
            SELECT
                MAX(T0."TaxDate")
            FROM
                "OWTR" T0
                INNER JOIN "WTR1" T1 ON T0."DocEntry" = T1."DocEntry"
            WHERE
                T1."ItemCode" = A."ItemCode"
                AND T1."FromWhsCod" = H."WhsCode"
        ) AS "ULTIMO_MOVIMIENTO",
        (
            SELECT
                MAX(T3."TaxDate")
            FROM
                "OIGN" T3
                INNER JOIN "IGN1" T4 ON T3."DocEntry" = T4."DocEntry"
            WHERE
                T4."ItemCode" = A."ItemCode"
                AND T4."WhsCode" = H."WhsCode"
        ) AS "ULTIMA_ENTRADA",
        O."U_GSP_Name",
        P."Name" AS "COLLECTION" ROM "OITM" A
        LEFT JOIN "OCRD" B ON A."CardCode" = B."CardCode"
        LEFT JOIN "@TI_COLORITEMS" C ON A."U_TI_COLORCODE" = C."Code"
        LEFT JOIN "@TI_SIZEITEMS" D ON A."U_TI_SIZEITEMS" = D."Code"
        LEFT JOIN "OITW" F ON A."ItemCode" = F."ItemCode"
        and A."DfltWH" = F."WhsCode"
        LEFT JOIN "@GSP_TCSEASON" G ON A."U_GSP_Season" = G."Code"
        LEFT JOIN "OITW" H ON A."ItemCode" = H."ItemCode"
        INNER JOIN "OWHS" I ON H."WhsCode" = I."WhsCode"
        LEFT JOIN "@GSP_TCMODEL" J ON J."U_GSP_REFERENCE" = "SPLIT_WITH_DELIMITER"(A."ItemCode", '_', 1)
        LEFT JOIN "@GSP_BSSECCION" K ON J."U_GSP_MATERIAL" = K."Code"
        LEFT JOIN "@GSP_TCMATERIAL" M ON J."U_GSP_MATERIAL" = M."Code"
        LEFT JOIN "@GSP_TCMODELCOLOR" N ON J."Code" = N."U_GSP_ModelCode"
        LEFT JOIN "@GSP_TCCOLOR" O ON N."U_GSP_ColorCode" = O."Code"
        LEFT JOIN "@GSP_TCCOLLECTION" P ON J."U_GSP_COLLECTION" = P."Code"
        INNER JOIN "@TI_TIPOTEJIDO" Q ON A."U_TI_CODTIPOTEJIDO" = Q."Code"
        INNER JOIN "@TI_NOMBRECOMERCIAL" R ON A."U_TI_CODCOMERCIAL" = R."Code" HERE H."OnHand" <> 0