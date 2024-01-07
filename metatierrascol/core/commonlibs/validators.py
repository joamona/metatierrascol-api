from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth import password_validation

def isValidFileExtension(filename:str, valid_extensions_list:list):
    import os
    ext = os.path.splitext(filename)[1]  # [0] returns path+filename
    if not ext.lower() in valid_extensions_list:
        return False
    else:
        return True

def isValidEmail(email):
    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        return False
    return True 

def isValidPassword(psw, user):
    try:
        password_validation.validate_password(psw, user)
    except ValidationError as e:
        m=""
        for men in e.messages:
            m=m+men
        return {"ok":False, "messages": m}
    return {"ok":True, "messages": ''}