from sqlalchemy import create_engine
import pandas as pd
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\app\client\ELLAIA\product\19.0.0\client_1\bin")
engine = create_engine('oracle+cx_oracle://DAAMHAOUZ:DAAMHO2023uzA%@172.16.5.28:1521/TAYSSIRPROD')



query = """
SELECT d.LIBF_PROVINCE as "Province", d.LIBF_COMMUNE as "Commune", decode(mad.current_statut,'GENERE','NON ENCORE RETIRE','PAYE','RETIRE','VEROUILLE','EN COURS') as "Etat", count(*) as "Nombre"
  FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
 WHERE     mad.cnie = mi.cin
       AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
       AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
       group by mad.current_statut, d.LIBF_PROVINCE, d.LIBF_COMMUNE
       order by 1,2,3
"""


df = pd.read_sql(query, engine)


print(df)
