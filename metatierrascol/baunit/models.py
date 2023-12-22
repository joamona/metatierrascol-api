from django.db import models
from uuid import uuid4

class Baunit(models.Model):
    gid = models.IntegerField(primary_key=True, editable=False)

