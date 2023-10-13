#import os
#os.environ["DPI_DEBUG_LEVEL"] = "92"



import pandas as pd
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\app\client\ELLAIA\product\19.0.0\client_1\bin")
dsn_tns = cx_Oracle.makedsn('172.16.5.28', '1521', service_name='TAYSSIRPROD')
conn = cx_Oracle.connect(user='WHATSAPPLOG', password='Whats5987M', dsn=dsn_tns)


query = """
SELECT TO_CHAR(CREATED_AT, 'YYYY-MM-DD') AS "Date", COUNT(DISTINCT CNIE) AS "Authenticated_Clients"
FROM TRANSACTIONS
WHERE CNIE IS NOT NULL
GROUP BY TO_CHAR(CREATED_AT, 'YYYY-MM-DD')
ORDER BY "Date"
"""

df = pd.read_sql(query, conn)
conn.close()
print(df)
