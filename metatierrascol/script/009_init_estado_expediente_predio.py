from core.commonlibs.addCodeList import addCodeList
l=['Recibido', 'En proceso', 'Errores para corregir', 'Revisado todo ok', 'Enviado ANT']
addCodeList(tableName='estado_expediente', valuesList=l)
print('Tabla codelist.estado_expediente inicializada')

