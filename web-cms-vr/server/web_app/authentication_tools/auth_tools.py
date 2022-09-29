from django.conf import settings
import jwt

def authenticate(request,settings):
    try:
        decoded = jwt.decode(
        request.COOKIES['access_tkn'],
        settings.SIMPLE_JWT['SIGNING_KEY'],
        settings.SIMPLE_JWT['ALGORITHM'],
        audience=settings.SIMPLE_JWT['AUDIENCE'])

    except Exception as e:
        return False, str(e)
    
    return True, decoded

def authenticateInstructor(request,settings):
    tkn_verified,payload = authenticate(request,settings)
    
    if(tkn_verified == False):
        return False,False,payload
    
    if(payload['role'] == 'INSTRUCTOR'):
        return tkn_verified,True,payload

    return tkn_verified,False,payload


def authenticateStudent(request,settings):
    tkn_verified,payload = authenticate(request,settings)
    
    if(tkn_verified == False):
        return False,False,payload
    
    if(payload['role'] == 'STUDENT'):
        return tkn_verified,True,payload

    return tkn_verified,False,payload


