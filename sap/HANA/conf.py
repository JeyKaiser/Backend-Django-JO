from hdbcli import dbapi

from JO_System_Project.settings import HANA_DB_ADDRESS, HANA_DB_PASS, HANA_DB_PORT, HANA_DB_USER 

#losdatosdeconexionalabasededatosdehanna

hana_dbs = (
    'SBOJOZF',
    'SBOJOCOL',
    'SBOJOZFLLC',
    'SBOJOEUSLU',
    # 'PRUEBASJOZF',
    'SBOPRUEBASJOZFLLC', 
)

conn = dbapi.connect(   
    currentschema = 'SBOJOZF',
    address = HANA_DB_ADDRESS, 
    port = HANA_DB_PORT,
    user = HANA_DB_USER, 
    password = HANA_DB_PASS,
)

databases = []

try:
    SBOJOZF = dbapi.connect(   
        currentschema = 'SBOJOZF',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )

    databases.append((SBOJOZF))
except:
    print("No hay conexión con base de datos SBOJOZF")


try:
    SBOJOCOL = dbapi.connect(   
        currentschema = 'SBOJOCOL',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )
    databases.append((SBOJOCOL))
except:
    print("No hay conexión con base de datos SBOJOCOL")


try:
    SBOJOZFLLC = dbapi.connect(   
        currentschema = 'SBOJOZFLLC',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )
    databases.append((SBOJOZFLLC))
except:
    print("No hay conexión con base de datos SBOJOCOL")


try:
    SBOJOEUSLU = dbapi.connect(   
        currentschema = 'SBOJOEUSLU',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )
    databases.append((SBOJOEUSLU))
except:
    print("No hay conexión con base de datos SBOJOCOL")


try:
    SBOPRUEBASJOZFLLC = dbapi.connect(   
        currentschema = 'SBOPRUEBASJOZFLLC',# 'SBOJOZFLLC',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )
    databases.append((SBOPRUEBASJOZFLLC))
except:
    print("No hay conexión con base de datos SBOJOCOL")





try:
    SBOPINK = dbapi.connect(   
        currentschema = 'SBOPINK',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )
    databases.append((SBOPINK))
except:
    print("No hay conexión con base de datos SBOPINK")

try:
    PRUEBASJOZF = dbapi.connect(   
        currentschema = 'PRUEBASJOZF',
        address = HANA_DB_ADDRESS, 
        port = HANA_DB_PORT,
        user = HANA_DB_USER, 
        password = HANA_DB_PASS,
    )
except:
    print("No hay conexión con base de datos PRUEBASJOZF")