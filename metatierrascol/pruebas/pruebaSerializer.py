from baunit.serializers import BaunitSerializer
d={
    "nombre":"nombre",
    "departamento":1,
    "provincia":1,
    "sector_predio":1,
    "municipio": "El Encanto",
    "tipo":"1",
    "complemento":"complemento2"
}

s=BaunitSerializer(data=d)
r=s.is_valid()
print(r)
print(s.errors)
print(s.data)
print(s.validated_data)
