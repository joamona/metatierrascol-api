
import os, sys
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print(BASE_DIR)
print(sys.path)
from core.commonlibs.emails import emailNewUserEmailConfirm

from metatierrascol import settings

print(settings.EMAIL_HOST)
print(settings.EMAIL_USE_TLS)
print(settings.EMAIL_PORT)
print(settings.EMAIL_HOST_USER)
print(settings.EMAIL_UPV)
print(settings.EMAIL_HOST_PASSWORD)
print(settings.EMAIL_FROM)


#emailNewUserEmailConfirm(1,'joamona@cgf.upv.es','aaaaaaaa')

