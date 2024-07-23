from django.db import connection
from pgOperations.pgOperations import PgConnection, PgOperations, FieldsAndValues

oc=PgConnection(connection)
pgo=PgOperations(oc, global_print_queries=True)


print("Añadiendo nuevas settings para la gestión de nuevos usuarios")
fa=FieldsAndValues({
    'parameter_name':'enviar_email_cuando_un_usuario_sube_un_predio',
    'parameter_value': 'True',
    'help_en':'If True, sends an email to the users on a user upload a property a los usuarios del grupo receptor_email_usuario_sube_predio',
    'help_es': 'Si es True se envía un email a los usuarios del grupo receptor_email_usuario_sube_predio'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

fa=FieldsAndValues({
    'parameter_name':'enviar_email_cuando_un_usuario_se_registre',
    'parameter_value': 'True',
    'help_en':'If True, sends an email to the users in the group receptor_email_nuevos_usuarios',
    'help_es': 'Si es True se envía un email a los usuarios del grupo receptor_email_nuevos_usuarios'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

fa=FieldsAndValues({
    'parameter_name':'enviar_email_cuando_un_usuario_confirma_su_email',
    'parameter_value': 'True',
    'help_en':'Users in the group receptor_email_usuario_confirma_email will receive an email on a user comfirms his email',
    'help_es': 'Los usuarios en el grupo receptor_email_usuario_confirma_email reciben un email de aviso cuando un usuario confirma su email'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

fa=FieldsAndValues({
    'parameter_name':'auto_activar_usuario_cuando_confirme_email',
    'parameter_value': 'False',
    'help_en':'When a user comfirms email automatically will be activate',
    'help_es': 'Cuando un usuario active su email, automáticamente será activado'})
pgo.pgInsert(table_name='core.appsettings',fieldsAndValues=fa)

print("Nuevas settings añadidas")