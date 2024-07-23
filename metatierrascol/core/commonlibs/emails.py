from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import mail

from metatierrascol import settings
from . import generalModule

def emailNewUserEmailConfirm(user_id, username, email_confirm_token):

    url_confirm = settings.API_URL + 'core/email_confirm_token/?id=' + str(user_id) + "&email_confirm_token=" + email_confirm_token    
    subject = 'MetaTierras Colombia. Confirmación de email'
    message = f"""Querido usuario,
    
Tiene que confirmar su email para ser dado de alta en el sistema. Por favor haga click en el siguiente link. Si no se abre el navegador cópielo manualmente en él. Para poder entrar en el sistema y añadir datos debe esperar a que el elquipo de MetaTierras active su cuenta. Cuando esto ocurra recibirá un email de confirmación.

{url_confirm}

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    email_from = settings.EMAIL_UPV
    recipient_list = [username]
    send_mail( subject, message, email_from, recipient_list )
 
def emailUserDeactivationAccount(username):
    email_from = settings.EMAIL_UPV
    subject = 'Su cuenta en MetaTierras Colombia ha sido desactivada'
    message = f"""Querido usuario,
    
Sentimos informale de que su cuenta ha sido desactivada, y ya no podrá entrar en el sistema hasta que sea reactivada. Por favor contacte con nosotros en  {settings.EMAIL_UPV} para más información.

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    recipient_list = [username]
    send_mail( subject, message, email_from, recipient_list )

def emailUserActivationAccount(username):
    subject = 'Activación de su cuenta en MetaTierras Colombia'
    message = f"""Querido usuario,
    
Nos complace informarle de que su cuenta en MetaTierras, {settings.WEB_URL}, ha sido activada. Ya puede entrar en el sistema y subir datos.

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    email_from = settings.EMAIL_UPV
    recipient_list = [username]
    send_mail(subject, message, email_from, recipient_list)



def alertUserConfirmedEmail(user_id, username, recipient_list):

    url_estatus = settings.API_URL + '/admin/auth/user/' + str(user_id) + '/'
    subject = 'MetaTierras Colombia. Un usuario confirmó su email'

    if generalModule.getSetting('auto_activar_usuario_cuando_confirme_email').lower()=="true":
        message = f"""Querido usuario,
    
Le avisamos de que el usuario {username} acaba de confirmar su email.
Su cuenta ha sido automáticamente activada.
Puede revisar su estatus en {url_estatus}.

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    else:
        message = f"""Querido usuario,
    
Le avisamos de que el usuario {username} acaba de confirmar su email.
Puede revisar su estatus en {url_estatus}.

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    email_from = settings.EMAIL_UPV
    #send_mail( subject, message, email_from, recipient_list )
    myMassSendMail(subject=subject,message=message,email_from=email_from, recipient_list=recipient_list)

def alertUserJustregistered(user_id, username, recipient_list):

    url_estatus = settings.API_URL + '/admin/auth/user/' + str(user_id) + '/'
    subject = 'MetaTierras Colombia. Un usuario se acaba de registrar'
    message = f"""Querido usuario,
    
Le avisamos de que el usuario {username} acaba registrarse.
Puede revisar su estatus en {url_estatus}.

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    email_from = settings.EMAIL_UPV
    myMassSendMail(subject=subject,message=message,email_from=email_from, recipient_list=recipient_list)

def avisaZipDisponibleDescarga(codigo_acceso, username, tamaño, data):
    destinatarios = generalModule.getAllUserEmailsInGroup('receptor_email_usuario_sube_predio')
    if generalModule.getSetting('enviar_email_al_usuario_que_sube_el_predio').lower()=='true':
        emailCurrentUser=generalModule.getUserEmailFromUsername(username)
        destinatarios.append(emailCurrentUser)
    
    #destinatarios=[]
    #for row in r:
    #    destinatarios.append(row['email'])
    
    enlace = settings.API_URL + 'source/descarga_zip_codigo_acceso/' + codigo_acceso + '/'
    borrar=generalModule.getSetting('borrar_fichero_zip_al_descargar')
    if borrar.lower() == 'true':
        aviso = 'Por seguridad, el fichero SERÁ ELIMINADO después de la primera descarga'
    else:
        aviso = 'El fichero NO será eliminado después de la primera descarga'
    

    subject='Proyecto MetaTierras Colombia. Fichero de datos de campo disponible para la descarga'
    
    message=f"""Querido usuario,

El usuario {username} acaba de subir un fichero con una medición.
Puede descargar el fichero ({tamaño} mb) en el siguiente enlace:

    {enlace}

    {aviso}

    Datos del predio:
        Nombre: {data['nombre']}
        Departamento: {data['departamento']}
        Provincia: {data['provincia']}
        Sector: {data['sector_predio']}
        Numero predial: {data['numero_predial']}
        Tipo: {data['tipo']}
        Complemento: {data['complemento']}

Saludos cordiales,
El equipo de MetaTierras Colombia, Universitat Politècnica de València, en colaboración con la Fundación Forjando Futuros.

AVISO LEGAL: La información que se puede obtener con este mensaje es información personal de los 
usuarios interesados en el expediente de regualrización de tierras. Usted se compromete a hacer un
buen uso de dicha información, siempre en interés de los usuarios que aparecen en el expediente,
eximiento al equipo de la Universitat Politècnica de València de cualquier responsabilidad, derivada
del uso de dicha información.

    """
    email_from = settings.EMAIL_UPV
    recipient_list=destinatarios
    myMassSendMail(subject=subject,message=message,email_from=email_from, recipient_list=recipient_list)

def myMassSendMail(subject, message, email_from, recipient_list):
    recipient_list = list( dict.fromkeys(recipient_list))#remove duplicated emails

    if settings.DEBUG:
        print('Enviando email')
        print('Destinatarios:', recipient_list)
        print('Subject', subject)
        print('Email from: ', email_from)

    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject=subject,
            body=message,
            from_email=email_from,
            bcc=recipient_list,
            connection=connection,
        ).send()
    print('----Email enviado-----')


def checkEmailToken(email,reset_url):

    subject = 'MetaTierras Colombia. Restablecimiento de contraseña'
    message = f"""Querido usuario,
    
Haga click en el siguiente link para poder reestablecer su contraseña:

{reset_url}

--
Saludos,
El equipo de MetaTierras Colombia.
{settings.WEB_URL}
"""
    email_from = settings.EMAIL_UPV
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )