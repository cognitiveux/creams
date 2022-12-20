import base64
from re import sub
from turtle import distance
from django.conf import settings
from django.utils.timezone import now
from django.db.models import F, ExpressionWrapper, DecimalField
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .application_error import ApplicationError
from .authentication_tools import auth_tools as at

from math import radians, cos, sin, asin, sqrt
from .models import *
from .logging import logger as log
from web_app.models import (
    ResetPassword,
    Users,
)

import ssl
import smtplib
import uuid


EMAIL_BODY = """
Hi,\n\nTo verify your CREAMS {} please use the following code:{}\n\n
If you did not request this code, please let us know.\n\nThanks,\nCreams Team
"""

EMAIL_HTML="""
<html>
    <body>
        <p>Hi,<br><br>
            To verify your CREAMS  {}
            please use the following code:<br><br>
            <strong>{}</strong>
        </p>
        <p>If you did not request this code, please let us know.</p><br><br>
        <p>Thanks,<br>
        Creams Team</p>
    </body>
</html>
"""

def build_email_object(verification_type, verification_code, fromaddr, toaddr):
    """
    Args:
        verification_type (str):
            The verification type , which is included as a key in settings.VERIFICATION_TYPES
            and settings.MODEL_MAPPING
        verification_code (str):
            The verification code that will be displayed in the email
        fromaddr (str):
            The email of the sender
        toaddr (str):
            The email of the receiver
    Returns:
        MIMEMultipart object with the message.
        Text built lives in views_utils.EMAIL_BODY, views_utils.EMAIL_HTML
    """
    msg = MIMEMultipart("alternative")
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = settings.VERIFICATION_TYPES.get(verification_type).get('msg_subject')
    text = EMAIL_BODY.format(settings.VERIFICATION_TYPES.get(verification_type).get('literal'),verification_code)
    html = EMAIL_HTML.format(settings.VERIFICATION_TYPES.get(verification_type).get('literal'),verification_code)
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)
    return msg

def generate_random_uuid(length=32):
    """
    Generates a random UUID as a ``length``-character hexadecimal string

        Returns:
            (str): The UUID
    """
    return uuid.uuid4().hex[0:length]


def get_ip_address(request):
    '''Returns the client's IP address from the `request` META attribute

        Args:
            request (rest_framework.request.Request): The request object

        Returns:
            ip (str): Client's IP address
    '''
    ip = None

    if isinstance(request, dict):
        x_forwarded_for = request['META']['HTTP_X_FORWARDED_FOR']

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request['META']['REMOTE_ADDR']
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

    return ip

def request_details(request):
    '''
    Returns details for the request as a string. This is a helper function for logging.

    Args:
        request (rest_framework.request.Request):
            The request object

    Returns:
        <ip> <user> if possible else <ip>
    '''
    username = None
    if isinstance(request, dict):
        user = request.get('user')
        if user:
            username =  user.get('username')
        else:
            username = request['data'].get('username')
    else:
        try:
            access_granted,decoded = at.authenticate(request,settings)
            username = decoded['sub']
        except Exception:
            username = None

    if not username:
        username = 'anonymous'

    return get_ip_address(request)+" - "+username+" - "


def serialize_request(request):
    '''
    Serializes a django.http.request object to be passed as a parameter in tasks

    Args:
        request (django.http.request):
            The request object that will be serialized
    Returns:
        dict:
            The serialized dictionary
    '''
    username = None

    try:
        username = request.user.email
    except Exception as e:
        try:
            username = request.user.get_username()
        except Exception as e:
            username = None

    # Only the required properties for logging are serialized
    result = {
        'user': {
            'username': username,
            'id': request.user.id,
        },
        'data': request.data,
        'META': {
            'HTTP_X_FORWARDED_FOR': request.META.get('HTTP_X_FORWARDED_FOR'),
            'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
            'HTTP_USER_AGENT': request.META.get('HTTP_USER_AGENT'),
            'HTTP_AUTHORIZATION': request.META.get('HTTP_AUTHORIZATION'),
        },
    }
    return result


def send_verification_email(email, verification_code, verification_type):
    """
    Sends an email containing the verification_code to the email
    Args:
        email (str): The email address.
        verification_code (str): The verification code.
        verification_type (str): The verification type.
    """
    log.info("Will send email to address: {}".format(email))
    fromaddr = settings.GLOBAL_SETTINGS.get('FROM_EMAIL')
    fromaddr_alias = settings.GLOBAL_SETTINGS.get('FROM_EMAIL_ALIAS')
    toaddr = email
    password = settings.GLOBAL_SETTINGS.get('EMAIL_PASSWORD')
    msg = build_email_object(verification_type, verification_code, fromaddr_alias, toaddr)

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(fromaddr, password)
            server.sendmail(
                fromaddr, toaddr, msg.as_string()
            )
            log.info("Email successfully sent to address: {}".format(email))
    except Exception as e:
        log.error("Failed to send verification email to address: {}. Reason: {}".format(email, str(e)))
        raise

# This function sorts a QuerySet based on its distance from a coordinate set.
def sortGeo(demo_list,lat,lon):
    artworks_list = {}
    cnt = 0
    for item in demo_list:
        artworks_list[cnt] = [item['lat'],item['lon'],item['id']]
        cnt = cnt + 1
        
    tmp_list = []
    for k, v  in artworks_list.items():      
        temp_ins = []
        temp_ins.append(v)
        temp_ins.append(k)
        tmp_list.append(temp_ins) 
        
    artworks_list = sorted(tmp_list, key=lambda x: geoDistance(float(lat),float(lon),x[0][0],x[0][1]))
    sorted_list = []
    for st in artworks_list:
        sorted_list.append(demo_list[st[1]])
        
    return sorted_list

# This function calculates the distance between two sets of (x,y) coordinates in the earth
def geoDistance(lat1,lon1,lat2,lon2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    # calculate the result
    return(c * r)
   
# This function transforms an image to a base64 encoded string
def getBase64(src):
    with open("media/" + src, "rb") as image_file:
        return base64.b64encode(image_file.read())
    
def changeExhibitionState(exh_id,new_state):
    Exhibition.objects.filter(id=exh_id).update(
    status= new_state
    )
    
def chechRole(user_id,role):
    
    
    return Users.objects.filter(id=user_id).values()[0]["role"] == role