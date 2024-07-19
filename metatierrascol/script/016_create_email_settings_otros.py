from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues

oc=PgConnection(connection)
pgo=PgOperations(oc, global_print_queries=True)


print("Añadiendo nuevas settings para la gestión de nuevos usuarios 2")

fa=FieldsAndValues({
    'parameter_name':'enviar_email_interesados_cuando_se_suba_su_predio',
    'parameter_value': 'True',
    'help_en':'When a new property is uploaded, alert the owners by email, and send links to watch and download',
    'help_es': 'Cuando un nuevo predio se sube, enviar un aviso a los propietarios con los links de visualización y descarga'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

fa=FieldsAndValues({
    'parameter_name':'enviar_email_al_usuario_que_sube_el_predio',
    'parameter_value': 'True',
    'help_en':'When a user uploads a property, send him an email with the links. Note that a user can upload properties of other owners',
    'help_es': 'Cuando un usuario sube un predio, enviarle un email con los enlaces de visualización y descarga. El usuario que sube el predio no tiene por qué ser el dueño del predio'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)


print("Nuevas settings añadidas")