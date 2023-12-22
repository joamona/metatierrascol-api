'''
Created on Dec 9, 2023

@author: joamona
'''

from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues

oc=PgConnection(connection)
po=PgOperations(pgConnection=oc, autoCommit=True, global_print_queries=True)
#snr_persona_titular_tipo

def addCodeList(tableName, valuesList):
#    cons='create table codelist.{tableName} (gid serial primary key, {tableName} varchar unique)'.format(tableName=tableName)
#    print(cons)
#    oc.cursor.execute(cons)
#    oc.commit()
    
    t='codelist.' + tableName
    for v in valuesList:
        d={tableName:v}
        fv=FieldsAndValues(d=d)
        po.pgInsert(table_name=t, fieldsAndValues=fv, str_fields_returning=None, print_query=True) 

    oc.commit()