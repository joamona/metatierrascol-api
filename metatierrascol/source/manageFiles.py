#ESTE MÓDULO FUNCIONA, PERO YA NO SE USA

import io
from django.http import HttpRequest

from baunit.serializers import BaunitSerializer
from .models import FicheroZip
from core.commonlibs import generalModule
from core.commonlibs.validators import isValidFileExtension

def uploadFile(request: HttpRequest):
    nombre = request.POST.get("nombre", '')
    departamento = request.POST.get('departamento')#se necesita el nombre, el serializador lo cambia por el id
    provincia=request.POST.get("provincia")
    sector_predio=request.POST.get("sector_predio")
    municipio = request.POST.get("municipio")
    numero_predial = request.POST.get("numero_predial", '')
    tipo = request.POST.get("tipo")
    complemento = request.POST.get("complemento", '')
    estado_expediente = 'Recibido'
    creado_por=request.user

    d={"nombre": nombre, "departamento": departamento, "provincia":provincia,
       "sector_predio":sector_predio, "municipio": municipio, 
       "numero_predial":numero_predial, "tipo":tipo,
       "complemento":complemento, "estado_expediente": estado_expediente,
       "creado_por":creado_por}

    s=BaunitSerializer(data=d)
    if s.is_valid():
        print('Es valido')
        baunit=s.save()
    else:
        print('s.errors')
        return s.errors

    filesObj = request.FILES.getlist('archivo')
    if len(filesObj) > 0:
        for f in filesObj:  #You have to upload the files from one to one
            name = f.name
            tamaño_maximo_fichero_zip_mb=float(generalModule.getSetting("tamaño_maximo_fichero_zip_mb"))
            size= f.size
            if size > (float(tamaño_maximo_fichero_zip_mb)*1000000):
                return {"mensaje": ["Fichero demasiado grande. Tamaño máximo permitido: {0} mb".format(tamaño_maximo_fichero_zip_mb)]}
            if not(isValidFileExtension(name,['.zip'])):
                    return {"mensaje":['La extensión del fichero debe ser .zip']}
            
            zip=FicheroZip()
            zip.creado_por_id = request.user.id
            zip.baunit_id =baunit.id
            zip.save()
            
            filename= str(baunit.id) + ".zip"#la ruta debe ser relativa a MEDIA_ROOT + lo que hayas puesto en 
                                        #la configuración de model.FileField
            #subprocess.run(['chmod', '771', tempFolder])
            
            zip.nombre_fichero.save(name=filename, content=io.BytesIO(f.read()), save=True)            
            zip.save()
            return {'mensaje': [f"Fichero guardado. Baunit ID: {baunit.id}"]}
    else:
        return {'mensaje': ["No habia ningún fichero en los datos"]}
         

# def downloadFile(request):
#     """
#     Receives by POST the gid and the filename: u other file of the model
#     returns the file.
#     Si settings.REAL_TIME_PDF_GENERATION_MODE==True, si es un PDF, Genera el fichero en tiempo real, lo envía y lo borra
#     Si settings.REAL_TIME_PDF_GENERATION_MODE==False, si es un PDF: 
#             - si el pdf no existe, genera el fichero en tiempo real, lo envía y NO lo borra
#             - si el pdf existe envía el fichero existente
#     Los ficheros de otro tipo deben existir siempre, simplemente los envía
#     """
#     pg=generalModule.getDjangoPg()
    
#     d=generalModule.getPostFormData(request)
#     if not(d):
#         return HttpResponse(status=400)#No hay datos en el post
    
#     gid=d.get("gid","")
#     if gid=="":
#         return HttpResponse(status=401)#no se ha especificado gid
    
#     fileToDownload=d['fileToDownload']#the file name to download
    
#     if not(generalModule.isAdministrator(request)):
#         if fileToDownload=='log.txt' or fileToDownload=='coordinates.txt':
#             return HttpResponse(status=402)
#             return JsonResponse({"ok":"false","message": "You must be administrator to download this file", "data":[]})
#         if not(generalModule.isOwnerOfCoordinatesFile(gid, request, pg)):
#             return HttpResponse(status=402)
#             return JsonResponse({"ok":"false","message": "You are not the owner of this report", "data":[]})
    
#     if not(generalModule.isAdministrator(request)):
#         if models.CoordinatesFile.objects.filter(gid=gid, deleted=True).exists():
#             return HttpResponse(status=402)
#             return JsonResponse({"ok":"false","message": "The report {0} has been deleted".format(gid), "data":[]})
#     return sendFile(gid, fileToDownload)


# #def downloadModelFileFunction(request, gid, fileToDownload):
# def downloadModelFileFromUrlFunction(token_url, fileToDownload):
#     """
#     Si settings.REAL_TIME_PDF_GENERATION_MODE==True, si es un PDF, Genera el fichero en tiempo real, lo envía y lo borra
#     Si settings.REAL_TIME_PDF_GENERATION_MODE==False, si es un PDF: 
#             - si el pdf no existe, genera el fichero en tiempo real, lo envía y NO lo borra
#             - si el pdf existe envía el fichero existente
#     Los ficheros de otro tipo deben existir siempre, simplemente los envía
#     """

#     if token_url is None or fileToDownload is None:
#         return HttpResponse(status=402)
    
#     pg=generalModule.getDjangoPg()
#     r=pg.pgOper.pgSelect(table_name='public.coordinates_file', string_fields_to_select="gid",cond_where="token_url=%s",list_val_cond_where=[token_url])
#     if len(r)==0:
#         return HttpResponse(status=402)
#         return JsonResponse({"ok":"false","message": "The provided url does not exist", "data":[]})
#     gid=r[0]["gid"]
#     return sendFile(gid, fileToDownload)


# def sendFile(gid, fileToDownload):
#     pg=generalModule.getDjangoPg()
#     if not fileToDownload in ['coordinates.txt','log.txt','report.txt','Results.pdf','Results_ES.pdf', 'Results_advanced.pdf','Results_advanced_ES.pdf', 'Registered_cloud.ply', 'Registered_mesh.ply','Ellipsoid_distances.ply', 'Registered_mesh.stl', 'Ellipsoid_distances_binary.ply']:
#         return HttpResponse(status=402)
#         return JsonResponse({"ok":"false","message": "The requested file has not an appropiate name", "data":[]})

#     r=pg.pgOper.pgSelect(table_name='public.coordinates_file', string_fields_to_select="gid,date, patientname, username",cond_where="gid=%s",list_val_cond_where=[gid])
#     if len(r) == 0:
#         return HttpResponse(status=402)

#     username=r[0]['username']
#     name=fileToDownload.split('.')[0]
#     extension=fileToDownload.split('.')[1]
#     patientname=r[0]["patientname"]
#     date=r[0]["date"]
#     dt=datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f')
#     year=str(dt.year)
#     month=generalModule.put0Before(str(dt.month))
#     day=generalModule.put0Before(str(dt.day))
#     hours=generalModule.put0Before(str(dt.hour))
#     minutes=generalModule.put0Before(str(dt.minute))
#     filename2 = patientname + '_' + name + '_' + year + month + day + '_' + hours + 'h_' + minutes + 'm.' + extension;
  
#     filename=settings.MEDIA_ROOT + '/' + str(gid) + "/" + fileToDownload
#     if settings.REAL_TIME_PDF_GENERATION_MODE:
#         if fileToDownload not in ['Results.pdf','Results_ES.pdf', 'Results_advanced.pdf','Results_advanced_ES.pdf']:
#             if not(os.path.isfile(filename)):
#                 return HttpResponse(status=402)
#                 return JsonResponse({"ok":"false","message": "The file {0} does not exist. Maybe the model is still being calculated. It takes about 15 minutes to calculate a model. Take a cofee.".format(fileToDownload), "data":[]})
#     else:#si no es REAL_TIME_PDF_GENERATION_MODE
#         if not(os.path.isfile(filename)):
#             if fileToDownload in ['Results.pdf','Results_ES.pdf', 'Results_advanced.pdf','Results_advanced_ES.pdf']:
#                 destinationFolder=settings.MEDIA_ROOT + '/' + str(gid) + "/"
#                 filename= settings.MEDIA_ROOT + '/' + str(gid) + "/" + fileToDownload
#                 if fileToDownload == 'Results.pdf':
#                     generate_report(gid=gid, report_type='Simple_EN', folder=destinationFolder , output_file_name=filename)
#                 elif fileToDownload == 'Results_ES.pdf':
#                     generate_report(gid=gid, report_type='Simple_ES', folder=destinationFolder , output_file_name=filename)
#                 elif fileToDownload == 'Results_advanced.pdf':
#                     generate_report(gid=gid, report_type='Advanced_EN', folder=destinationFolder , output_file_name=filename)
#                 elif fileToDownload == 'Results_advanced_ES.pdf':
#                     generate_report(gid=gid, report_type='Advanced_ES', folder=destinationFolder , output_file_name=filename)           
#             else:
#                 return HttpResponse(status=402)
#                 return JsonResponse({"ok":"false","message": "The file {0} does not exist. Maybe the model is still being calculated. It takes about 15 minutes to calculate a model. Take a cofee.".format(fileToDownload), "data":[]})

#     #print(filename)

#     #mimetypes.guess_type(filename)[0]
#     chunk_size = 8192
    
#     ##PONGO SIEMPRE application/pdf porque si no no añade content-length, y cuando se descarga
#     #no va el progress bar
#     if ".pdf" in fileToDownload:
#         contenttype="application/pdf"
#     else:
#         contenttype="application/pdf"    
    
#     if settings.REAL_TIME_PDF_GENERATION_MODE:
#         if fileToDownload in ['Results.pdf','Results_ES.pdf', 'Results_advanced.pdf','Results_advanced_ES.pdf']:
#             destinationFolder=settings.MEDIA_ROOT + '/' + str(gid) + "/"
#             filename= settings.MEDIA_ROOT + '/' + str(gid) + "/" + next(tempfile._get_candidate_names()) + '.pdf'  #devuelve algo así /ruta/gid/sdshjhf.pdf
#             if fileToDownload == 'Results.pdf':
#                 generate_report(gid=gid, report_type='Simple_EN', folder=destinationFolder , output_file_name=filename)
#             elif fileToDownload == 'Results_ES.pdf':
#                 generate_report(gid=gid, report_type='Simple_ES', folder=destinationFolder , output_file_name=filename)
#             elif fileToDownload == 'Results_advanced.pdf':
#                 generate_report(gid=gid, report_type='Advanced_EN', folder=destinationFolder , output_file_name=filename)
#             elif fileToDownload == 'Results_advanced_ES.pdf':
#                 generate_report(gid=gid, report_type='Advanced_ES', folder=destinationFolder , output_file_name=filename)
#             response = StreamingHttpResponse(FileDeleteWrapper(filepath = filename,filelike=open(filename, 'rb'),blksize=chunk_size),content_type=contenttype)
#         else:
#             response = StreamingHttpResponse(FileWrapper(open(filename, 'rb'), chunk_size),content_type=contenttype)
#     else:
#         response = StreamingHttpResponse(FileWrapper(open(filename, 'rb'), chunk_size),content_type=contenttype)

#     incrementDownloadedFileCounter(fileToDownload=fileToDownload, username=username, pg=pg)
#     response['Content-Length'] = os.path.getsize(filename)    
#     response['Content-Disposition'] = "attachment; filename=%s" % filename2
#     return response


