from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues

oc=PgConnection(connection)
pgo=PgOperations(oc, global_print_queries=True)


print("Añadiendo setting. Número máximo de filas devueltas")

fa=FieldsAndValues({
    'parameter_name':'numero_maximo_de_filas_recuperadas',
    'parameter_value': '5000',
    'help_en':'To retrieve many rows consumes many server resources. Better to limit it',
    'help_es': 'Recuperar muchas filas puede ser costoso para el servidor. Es mejor limitarlo'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

print("Número máximo de filas devueltas añadido")