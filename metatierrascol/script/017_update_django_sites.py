#This script is to be able to set the site to properly render
#the site name in the email of password reset
"""
import os

API_URL = os.getenv('API_URL')
FORCE_SCRIPT_NAME= os.getenv('FORCE_SCRIPT_NAME')

site = API_URL.replace(FORCE_SCRIPT_NAME, '')#removes 'api/' from the url
site = site.replace('https://', '')
site = site.replace('http://', '')
#site = site[:-1]#removes the final '/'

from pgOperations.pgOperations import FieldsAndValues, WhereClause
from core.commonlibs.generalModule import getDjangoPg

print(f"Actializando el nombre del sitio para password reset: {site}")
pgo = getDjangoPg()

fieldsAndValues=FieldsAndValues({'domain':site, 'name':site})
pgo.pgUpdate('public.django_site',fieldsAndValues)

print(f"Sitio insertado")
"""