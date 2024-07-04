from core.serializers import AppUserSerializer
d={
'user':1, 
'data_acceptation':False, 
'notification_aceptation':False, 
'interest':'interes',
'email_confirm_token':'sdfadfasdfñlafkjñas'

}

s=AppUserSerializer(data=d)
r=s.is_valid()
print(r)
print(s.errors)
print(s.validated_data)
if (s.is_valid()):
    print(s.save())
