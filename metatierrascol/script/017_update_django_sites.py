#This script is to be able to set the site to properly render
#the site name in the email of password reset

import os

API_URL = os.getenv('API_URL')
FORCE_SCRIPT_NAME= os.getenv('FORCE_SCRIPT_NAME')

site = API_URL.replace(FORCE_SCRIPT_NAME, '')#removes 'api/' from the url
site = site.replace('https://', '')
site = site.replace('http://', '')
site = site[:-1]#removes the final '/'

from pgOperations.pgOperations import FieldsAndValues, WhereClause
from core.commonlibs.generalModule import getDjangoPg

print(f"Insertando nombre del sitio para password reset: {site}")
pgo = getDjangoPg()

whereClause=WhereClause('id=%s',[1])
fieldsAndValues=FieldsAndValues({'domain':'localhost:8000', 'name':'localhost:8000'})
pgo.pgUpdate('public.django_site',fieldsAndValues,whereClause)

if site != 'localhost:8000':
    print('Site for password reset SET in PRODUCTION')
    fieldsAndValues=FieldsAndValues({'domain':site, 'name':site})
    pgo.pgInsert('public.django_site',fieldsAndValues)
else:
    print('Site for password reset NOT SET in PRODUCTION')
    print('Please replace site name in the second row in django_site')
    fieldsAndValues=FieldsAndValues({'domain':'replace_by_your_production_site', 'name':'replace_by_your_production_site'})
    pgo.pgInsert('public.django_site',fieldsAndValues)

print(f"Sitio insertado")
