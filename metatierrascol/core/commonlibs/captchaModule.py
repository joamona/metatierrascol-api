'''
Created on 5 nov. 2020

@author: joamona
'''
from django import forms
from captcha.fields import CaptchaField
from django.shortcuts import render

class CreateCaptchaTestForm(forms.Form):
    """
    Creates the captcha in the database
    """
    captcha = CaptchaField()
    
def getCaptchaFieldsFromHtmlForm(htmlForm):
    """
    htmlForm is:

    <img src="/captcha/image/fe022749653f9ce0454ce2feff6d680fc1e594f5/" alt="captcha" class="captcha" />
metatierrascol-1  | <input type="hidden" name="captcha_0" value="fe022749653f9ce0454ce2feff6d680fc1e594f5" 
required id="id_captcha_0" autocomplete="off"><input type="text" name="captcha_1" required id="id_captcha_1" autocapitalize="off" autocomplete="off" autocorrect="off" spellcheck="false">

    renders the form and gets the fields {'csrmidlewaretoken':csrmidlewaretoken, 'srcImg': srcImg, 'captcha_0': captcha_0}
    searching in the html code. 
    Returns: a dict --> {'srcImg': srcImg, 'captcha_0': captcha_0}
    """
    
    srcImgInitialPosition=htmlForm.find('<img src="') + 10
    srcImgFinalPosition=htmlForm.find('" alt="captcha"', srcImgInitialPosition)
    
    if srcImgInitialPosition == 9 or srcImgFinalPosition == -1:
        raise Exception("Error in  getCaptchaFieldsFromHtmlForm. Error in getting srcImg")
    srcImg=htmlForm[srcImgInitialPosition:srcImgFinalPosition]
    
    captcha_0_InitialPosition=htmlForm.find('name="captcha_0" value="') + 24
    captcha_0_FinalPosition=htmlForm.find('" required id="id_captcha_0"')
    
    if captcha_0_InitialPosition == 23 or captcha_0_FinalPosition == -1:
        raise Exception("Error in  getCaptchaFieldsFromHtmlForm. Error in getting captcha_0")
    captcha_0=htmlForm[captcha_0_InitialPosition:captcha_0_FinalPosition]
     
    return {'srcImgCaptcha': srcImg, 'captcha_0': captcha_0}

def checkCaptchaFunction(dCaptcha):
    """
    Checks the user answer
    """
    #dcaptcha es un diccionario 
    #{
    #            csrfmiddlewaretoken: zdZPbQO3nItl9JQSW1B4fIWtzyNhKTRfLIgF17eOTqXa94qG40Yy5SteGrq7VmRN
    #            captcha_0: cf4ce659b285c204e19b6236a3247cb496cf05be
    #            captcha_1: HPVO  --> The user answer
    #}
    form = CreateCaptchaTestForm(dCaptcha)
    if form.is_valid():
        return True
    else:
        return False

def createCaptchaFunction(request):
    """
    Creates the captcha in the database and returns a dict with csrmidlewaretoken, srcImgCaptcha, captcha_0
    with the srcImg you can get the captcha in a form. To check the value introduced by the user
    use, in the login, or in the addUser the function checkCaptcha, by passing csrmidlewaretoken, captcha_0 and captcha_1
    in a dictionary. The captcha_1 is the user answer about the captcha img
    the checkCaptcha returns true or false
    """
    form = CreateCaptchaTestForm()
    a=render(request, 'captcha.html', {'form': form})
    htmlForm = a.content.decode('utf-8')
    d = getCaptchaFieldsFromHtmlForm(htmlForm)
    return {"ok":"true","message": "Captcha received", "data":[d]}
