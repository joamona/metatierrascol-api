from django.db import models
from uuid import uuid4

from codelist import models as codelist_models

class Baunit(models.Model):
    gid = models.IntegerField(primary_key=True, editable=False)
    uuid = models.UUIDField(unique=True, editable=False, default= uuid4, null=False)
    nombre = models.TextField(max_length=100)
    departamento = models.ForeignKey(codelist_models.Departamento, on_delete=models.CASCADE, null=False)
    sector_predio = models.ForeignKey(codelist_models.Sector,on_delete=models.CASCADE, null=False)
    municipio = models.ForeignKey(codelist_models.Municipio,on_delete=models.CASCADE, null=False)
    numero_predial = models.TextField(max_length=50)
    


