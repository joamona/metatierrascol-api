import json

from django.views import View
from django.http import JsonResponse
from . import manageFiles

#las vistas de clase normales también requieren el token
class AñadeFicheroZip(View):
    def post(self, request):
        r=manageFiles.uploadFile(request)
        return JsonResponse(r)