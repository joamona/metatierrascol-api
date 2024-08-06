from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues

oc=PgConnection(connection)
pgo=PgOperations(oc, global_print_queries=True)


print("Añadiendo setting. Configuración envío de emails al activar-desactivar usuarios")

fa=FieldsAndValues({
    'parameter_name':'enviar_email_al_activar_desactivar_usuarios',
    'parameter_value': 'True',
    'help_en':'Send an email of alert to the affected user on activate - deactivate its account. If its account is deactivated he can not login',
    'help_es': 'Enviar email de aviso al usuario cuando se active o desactive su cuenta. Si su cuenta está desactivada no puede iniciar sesión'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

print("Configuración añadida añadido")