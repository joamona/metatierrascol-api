from django.core.mail import send_mail
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

    if generalModule.getSetting('auto_activar_usuario_cuando_confirme_email')=="True":
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
    send_mail( subject, message, email_from, recipient_list )

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
    send_mail( subject, message, email_from, recipient_list )