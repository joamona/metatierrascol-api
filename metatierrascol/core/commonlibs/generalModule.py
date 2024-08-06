import json

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http.request import HttpRequest
from django.utils import timezone
from django.core.mail import send_mail
from django.db import connection

from pgOperations import pgOperations as pg
from pgOperations.pgOperations import WhereClause

from metatierrascol import settings


def getDjangoPg()->pg.PgOperations:
    pgc: pg.PgConnection = pg.PgConnection(connection)
    pgo: pg.PgOperations = pg.PgOperations(pgc, autoCommit=True,global_print_queries=settings.DEBUG)
    return pgo

def getDjangoCursor():
    return connection.cursor()

def getSettingsFunction(request):
    pgo=getDjangoPg()
    r=pgo.pgSelect(table_name="core.appsettings", string_fields_to_select="parameter_name,parameter_value")
    return {"ok":"true","message": "Settings successfully retrieved", "data":r}

def getSetting(parameterName):
    pgo=getDjangoPg()
    cond_where = WhereClause(where_clause="parameter_name=%s",where_values_list=[parameterName])
    r=pgo.pgSelect(table_name="core.appsettings", string_fields_to_select="parameter_value",whereClause=cond_where)
    return r[0]["parameter_value"]        

def isAdministrator(request):
    user=request.user
    return user.groups.filter(name='admin').exists()

def isNeighbor(user: User):
    return user.groups.filter(name='neighbors').exists()

def getUserGroups(user: User):
    l = user.groups.values_list('name',flat = True) # QuerySet Object
    return list(l)

def getUserGroupsToString(user: User):#devuelve una cadena 'grupo1, grupo2, ...'
    l = user.groups.values_list('name',flat = True) # QuerySet Object
    l =list(l)
    return stringListToString(l)

def getUserGroupsToString_fromUsername(username):
    user=User.objects.get(username=username)
    return getUserGroupsToString(user)

def getUserGroups_fromUsername(username):
    user=User.objects.get(username=username)
    return getUserGroups(user)

def stringListToString(l:list):#devuelve una cadena 'grupo1, grupo2, ...'
    s=""
    for g in l:
        s = s + g + ", "
    s=s[:-2]
    return s

def getGroupMembers(group_name):
    users=User.objects.filter(groups__name=group_name)
    l=[]
    for u in users:
        l.append(u.username)
    return l
    
def getUserCountry(username):
    """
    Returns the country or None
    """
    pg=getDjangoPg()
    r=pg.pgOper.pgSelect(table_name="public.app_user", string_fields_to_select="country_name", cond_where="username = %s", list_val_cond_where=[username])
    if r is None:
        return None
    if len(r) != 1:
        return None
    return r[0].get('country_name', None)    

def getCodelistFunction(codelist,pg):
    table_name="codelist." + codelist
    column_name=codelist
    r=getAllValuesInColumnFunction(table_name,column_name,pg)
    return r

def getAllValuesInColumnFunction(table_name, column_name,pg):
    codeList=pg.pgOper.pgSelect(table_name=table_name, string_fields_to_select=column_name,cond_where=None,list_val_cond_where=None,limit="1000")
    if codeList is None:
        return {"ok":"false","message": "There are not data in the column {0} of the table {1}".format(column_name,table_name), "data":""}
    else:
        return {"ok":"true","message": "{0} rows retrieved".format(len(codeList)), "data":codeList}

def getAllValuesInTable(table_name, pg):
    r=pg.pgOper.pgSelect(table_name=table_name, string_fields_to_select='*',cond_where=None,list_val_cond_where=None,limit="1000")
    return r

def getPostFormData(request: HttpRequest):
    """
    returns none if there is not POST data
    
    If is Angular who sends the post data request.POST is empty. The data is in
    request.body
    
    d=request.POST.get("form_data","")#caso no Angular
    if d!="":
        d=json.loads(d)
    else:
        #the data has been sent by angular
        d=json.loads(request.body.decode('utf-8'))
        d=d["form_data"]       
    return d
    """

    return request.POST

    js=request.POST.get("form_data","")
    d=None
    if js != "":
        d=json.loads(js)
    else:
        if len(request.body) > 0:
            js=request.body.decode('utf-8')
            d=json.loads(js)
            d2=d.get("form_data","")
            if d2 != "":
                d=d2
    if settings.DEBUG:
        #logger.debug('Here is the post data:\n %s', json.dumps(d, indent=4, sort_keys=True))  
        pass
    return d    

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        print(data)
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    o = User.objects.filter(id__in=uid_list)
    l=list(o)
    lf=[]
    for u in l:
        lf.append(u.username)
    print(lf)

def getOpenedKnoxSessions(username):
    pgo=getDjangoPg()
    wc=WhereClause('username=%s',[username])
    r=pgo.pgSelect('public.auth_user','id',wc)
    userId=r[0]['id']
    wc = WhereClause('user_id=%s',[userId])
    r=pgo.pgSelect('public.knox_authtoken','count(user_id)',wc,False)
    if len(r)>0:
        os=r[0][0]#user oppened session number
    else:
        os=0
    return os

def getUserEmailFromUsername(username):
    u=list(User.objects.filter(username=username))
    if len(u)>0:
        return u[0].email
    else:
        return ''

def getAllUsersInGroup(groupName:str):
    return list(User.objects.filter(groups__name=groupName))

def getAllUserEmailsInGroup(groupName:str):
    l=getAllUsersInGroup(groupName)
    le=[]
    for u in l:
        le.append(u.email)
    return le

def remove_id_fromDictKeys(d:dict)->dict:
    """
    Removes the last _id from the dictionary key names
    This is for use with pgOperations because, not as DRF,
    it returns the complete field values in the foreign field names
        DRF return 
            username
    but 
        pgOperations returns
            username_id
    Calling this function both methods are compatible
    """
    r={}
    for key,value in d.items():
        if key[-3:]=='_id':
            key2=key[:-3]
            r[key2]=value
        else:
            r[key]=value
    return r

        

def getUserModelFromUsername(username):
    """
    Returns a list with the user.
    An empty list if the user does not exist
    """
    return list(User.objects.filter(username=username))
