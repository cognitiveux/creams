from cmath import nan
from email import header
from .forms import *
from re import T
from celery.result import AsyncResult
from datetime import timedelta
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import (
	HttpResponse,
    HttpResponseRedirect,
)
from django.shortcuts import render  
from django.template import loader
from django.urls import reverse
from django.utils.timezone import now

from drf_yasg.utils import swagger_auto_schema

from rest_framework import (
    parsers,
    permissions,
    status,
)
from rest_framework.exceptions import ParseError
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.decorators import (
    permission_classes,
    api_view,
)

from rest_framework.permissions import(
    IsAuthenticated,
)

from creams_project.celery import (
    app,
)
from .application_error import ApplicationError
from .authentication_tools import auth_tools as at

from .logging import logger as log
from .models import *
from .serializers import *
from .status_codes import *
from .views_utils import (
    generate_random_uuid,
    request_details,
    send_verification_email,
    serialize_request,
    sortGeo,
    geoDistance,
    changeExhibitionState,
)

import jwt


BAD_REQUEST = "bad_request"
CONTENT = "content"
INTERNAL_SERVER_ERROR = "internal_server_error"
STRING_TYPE = "_str"
DICT_TYPE = "_dict"
ARRAY_TYPE = "_array"
BOOLEAN_TYPE = "_bool"
MESSAGE = "message"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
MISSING_REQUIRED_FIELDS = "missing_required_fields"
METHOD_NOT_ALLOWED = "method_not_allowed"
STATUS_CODE = "status_code"
RESOURCE = "resource"
RESOURCE_IS_ACTIVATED = "resource_is_activated"
RESOURCE_NAME = "resource_name"
RESOURCE_OBJ = "resource_obj"
RESOURCE_ID = "resource_id"
ARTWORK = "artwork"

TASK_STATUS = "task_status"

ALREADY_EXISTS_FIELDS = "already_exists_fields"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
ERROR_DETAILS = "error_details"
MISSING_REQUIRED_FIELDS = "missing_required_fields"


def index(request):
	template = loader.get_template('web_app/index.html')
	context = {
		'title': "Index title",
		'header_content': 'Index header content'
	}
	return HttpResponse(template.render(context, request))


class ArtworkCreate(CreateAPIView):
    """
    post:
    Creates a new artwork instance
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = ArtworkCreateSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('ArtworkCreate', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = ArtworkCreateSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        form = ArtWorkForm(request.POST, request.FILES)
                        form.save()
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'artwork'
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to create artwork."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class SampleAuthenticated(GenericAPIView):
    """
    post:
    Sample view that checks the JWT Authentication
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SampleAuthenticatedSerializer

    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['resource_not_allowed'],
        ['resource_not_found', 'user'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('SampleAuthenticated', response_types)

    @app.task(bind=True, time_limit=settings.CELERY_TASK_TIME_LIMIT)
    def sample_authenticated_task(self, data, request):
        response = {}
        log.debug("{} START".format(request_details(request)))
        serialized_item = SampleAuthenticatedSerializer(data=data)

        if not serialized_item.is_valid():
            log.debug("{} VALIDATION ERROR: {}".format(
                    request_details(request),
                    serialized_item.formatted_error_response()
                )
            )
            response = {}
            response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=False)
            response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
            return response
        else:
            try:
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                content[RESOURCE_NAME] = 'jwt'
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                return response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                return response

    @swagger_auto_schema(
        responses=response_dict,
        security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request". format(request_details(request)))

        try:
            result = self.sample_authenticated_task.delay(request.data, serialize_request(request))
            data = result.wait(timeout=None, interval=settings.CELERY_TASK_INTERVAL)
        except ParseError as e: # ParseError must be handled for endpoints that require authorization
            status_code, message = get_code_and_response(['bad_formatted_json'])
            content = {}
            content['message'] = message
            content['bad_formatted_fields'] = []
            content['missing_required_fields'] = []
            content['error_details'] = {
                'json': str(e)
            }
            return Response(content, status=status_code)
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, message = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: message
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


def visitor_dashboard(request):

    template = loader.get_template('web_app/visitor/landingpage.html')
    context = {
		'title': "Visitor Dashboard",
		'header_content': 'Index header content',
	}   
        
    return HttpResponse(template.render(context, request))


def submit_artwork(request):
	template = loader.get_template('web_app/submit_artwork.html')
	context = {
		'title': "Submit an artwork",
		'header_content': 'Index header content'
	}
	return HttpResponse(template.render(context, request))


def insertArtwork(request):
    form = ArtWorkForm()
    if request.method == 'POST':
        form = ArtWorkForm(request.POST,request.FILES)
        if form.is_valid():  
            form.save()  
        else:
            print("ERROR")
            print("========================================")
#
    return render(request, 'web_app/teacher/student_selection.html', {'form': form , 'id' : 2}) 


def submit_outdoor_artwork_to_exhibition_page(request):
    template = loader.get_template('web_app/submit_outdoor_artwork.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content'
	}
    
    return HttpResponse(template.render(context, request))


def outdoor_artwork_submit(request):
    form = OutdoorArtWorkForm()
    print("insert ME")
    print(request.POST)
    if request.method == 'POST':
        form = OutdoorArtWorkForm(request.POST)  
        if form.is_valid():  
            form.save()  
        else:
            print("ERROR")

    return render(request, 'web_app/teacher/student_selection.html', {'form': form , 'id' : 2})   


class getStudentsArtworks(RetrieveAPIView):
    """
    get: Get data of an artwork based on its id.
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    #permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'artwork'], 
    ]
    
    response_dict = build_fields('getStudentsArtworks', response_types)
    
    #parameters = openapi.Parameter(
        #'student-id',
        #in_=openapi.IN_QUERY,
        #description='The id of the artwork you want to fetch',
        #type=openapi.TYPE_INTEGER,
        #required=True,
    #)

    @swagger_auto_schema(
        responses=response_dict,
        #security=[{'Bearer': []}, ],
        #manual_parameters=[parameters]
    )

    def get(self, request):
        '''
        Get data of an artwork based on its id.
        '''
        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = UserSerializer(data=req_data)

            flag,stu,decoded = at.authenticateStudent(request,settings)
            if(flag == False  or stu == False):
                log.error("{} Internal error: {}".format(request_details(request), decoded))
                status_code, _ = get_code_and_response(['unauthorized'])
                content = {
                    MESSAGE: "Access token is invalid."
                }
                return Response(content, status=status_code)
                
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                st_id = req_data.get('student-id')
                art_list = Artwork.objects.filter(user_fk_id=decoded['user_id']).values()
                if not art_list:
                    raise ApplicationError(['resource_not_found', 'artwork_list'])
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                header_data = {}
                header_data["artworks"] = []
                for i in art_list:
                    data = {}
                    data["id"]          = i['id']
                    data["src"]         = i['src']
                    data["year"]        = i['year']
                    data["name"]        = i['name']
                    data["height"]      = i['height']
                    data["width"]       = i['width']
                    data["unit"]        = i['unit']
                    data["depth"]       = i['depth']
                    data["technique"]   = i['technique']
                    data["genre"]       = i['genre']
                    data["art_type"]    = i['art_type']
                    header_data["artworks"].append(data)
                content[RESOURCE_OBJ] = header_data     
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response

            
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to fetch artwork."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
     
        
class getArtwork(RetrieveAPIView):
    """
    get: Get data of an artwork based on its id.
    """
    serializer_class = ArtworkSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'artwork'], 
    ]
    
    response_dict = build_fields('getArtwork', response_types)
    
    parameters = openapi.Parameter(
        'artwork-id',
        in_=openapi.IN_QUERY,
        description='The id of the artwork you want to fetch',
        type=openapi.TYPE_INTEGER,
        required=True,
    )

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=[parameters]
    )

    def get(self, request):
        '''
        Get data of an artwork based on its id.
        '''
        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = ArtworkSerializer(data=req_data)
            
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                art_id = req_data.get('artwork-id')
                demo = Artwork.objects.filter(id=art_id).values()
                
                if not demo:
                    raise ApplicationError(['resource_not_found', 'artwork'])
                
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                
                artwork = demo[0]
                data = {}
                data["id"] = artwork['id']
                data["owner"] = artwork['user_fk_id']
                data["name"] = artwork['name']
                data["src"] = artwork['src']
                data["year"] = artwork['year']
                data["height"] = artwork['height']
                data["width"] = artwork['width']
                data["unit"] = artwork['unit']
                data["depth"] = artwork['depth']
                data["technique"] = artwork['technique']
                data["genre"] = artwork['genre']
                data["art_type"] = artwork['art_type']
                
                content[RESOURCE_OBJ] = data
                
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
                
            
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to fetch artwork."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
  
    
class getVRTemplate(RetrieveAPIView):
    """
    get: Get data of an artwork based on its id.
    """
    serializer_class = VR_TemplateSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'artwork'], 
    ]
    
    response_dict = build_fields('getVRTemplate', response_types)
    
    parameters = openapi.Parameter(
        'template-id',
        in_=openapi.IN_QUERY,
        description='The id of the vr template you want to fetch',
        type=openapi.TYPE_INTEGER,
        required=True,
    )

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=[parameters]
    )

    def get(self, request):
        '''
        Get data of a vr template based on its id.
        '''
        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = VR_TemplateSerializer(data=req_data)
            
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                temp_id = req_data.get('template-id')
                demo = VR_Templates.objects.filter(id=temp_id).values()
                
                if not demo:
                    raise ApplicationError(['resource_not_found', 'vr_template'])
                
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                
                temp = demo[0]
                data = {}
                data["id"] = temp['id']
                data["basis"] = temp['basis']
                data["name"] = temp['name']
                data["rooms"] = temp['rooms']
                
                content[RESOURCE_OBJ] = data
                
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
                
            
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to fetch vr template."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
 
        
class getOutdoorExhibition(RetrieveAPIView):
    """
    get: Get data of an outdoor exhibition based on its id.
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'outdoor_exhibition'], 
    ]
    
    response_dict = build_fields('getOutdoorExhibition', response_types)
    
    parameters = openapi.Parameter(
        'outdoor-exhibition-id',
        in_=openapi.IN_QUERY,
        description='The id of the outdoor exhibition you want to fetch',
        type=openapi.TYPE_INTEGER,
        required=True,
    )

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=[parameters]
    )
    def get(self, request, *args, **kwargs):
        '''
        Get data of an outdoor exhibition based on its id.
        '''
        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = OutdoorExhibitionSerializer(data=req_data)
        
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                exh_id = req_data.get('outdoor-exhibition-id')
                demo = OutdoorExhibition.objects.filter(id=exh_id).values()
            
                if not demo:
                    raise ApplicationError(['resource_not_found', 'outdoor_exhibition'])
            
                arts = OutdoorArtwork.objects.filter(exhibition_fk=exh_id).values()
            
                if not arts:
                    raise ApplicationError(['resource_not_found', 'outdoor exhibition artwork'])
            
         
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                exhibition = demo[0]
                header_data = {}
                header_data["id"] = exhibition['id']
                header_data["owner"] = exhibition['user_fk_id']
                header_data["start_date"] = exhibition['start_date']
                header_data["end_date"] = exhibition['end_date']
                header_data["description"] = exhibition['description']
                header_data["artworks"] = []
                for i in arts:
                    data = {}
                    data["lat"] = i['lat']
                    data["lon"] = i['lon']
                    demo2 = Artwork.objects.filter(id=i['artwork_fk_id']).values()
                    data["id"] = demo2[0]['id']
                    data["owner"] = demo2[0]['user_fk_id']
                    data["src"] = demo2[0]['src']
                    data["year"] = demo2[0]['year']
                    data["name"] = demo2[0]['name']
                    data["height"] = demo2[0]['height']
                    data["width"] = demo2[0]['width']
                    data["unit"] = demo2[0]['unit']
                    data["depth"] = demo2[0]['depth']
                    data["technique"] = demo2[0]['technique']
                    data["genre"] = demo2[0]['genre']
                    data["art_type"] = demo2[0]['art_type']
            
                    if not demo2:
                        raise ApplicationError(['resource_not_found', 'artwork'])
                    header_data["artworks"].append(data)
                
                content[RESOURCE_OBJ] = header_data
             
            
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
            
        
        except Exception as e:
           log.error("{} Internal error: {}".format(request_details(request), str(e)))
           status_code, _ = get_code_and_response(['internal_server_error'])
           content = {
               MESSAGE: "Failed to fetch outdoor exhibition."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
 
    
def create_outdoor(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    #access_tkn = "asd"
    try:
        decoded = jwt.decode(access_tkn, verify=False)
    except Exception as e:
        url = reverse('login')
        return HttpResponseRedirect(url)
    template = loader.get_template('web_app/create_outdoor.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content',
          'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role']
	}
    
    return HttpResponse(template.render(context, request))


def login_screen(request):
    template = loader.get_template('web_app/sign-in.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content'
	}
    
    return HttpResponse(template.render(context, request))


def signup_screen(request):
    template = loader.get_template('web_app/sign-up.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content',
        'organizations' : [oc[0] for oc in OrganizationModel.ORGANIZATION_CHOICES],
        'roles' : [r[0] for r in RoleModel.ROLE_CHOICES],
        'student_choices' : [r[0] for r in ClassAndLevelModel.STUDENT_CHOICES],
        'teacher_choices' : [r[0] for r in ClassAndLevelModel.TEACHER_CHOICES],

	}

    return HttpResponse(template.render(context, request))


def verifyAccount(request):
    template = loader.get_template('web_app/verifyemail.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content',
        'email': 'mbofos01@ucy.ac.cy'

	}

    return HttpResponse(template.render(context, request))


def vr_exhibition_demo(request):
    template = loader.get_template('web_app/vr-exhibitions/picasso/picasso.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content'
	}
    
    return HttpResponse(template.render(context, request))


def outdoor_exhibition_submit(request):
    form = OutdoorExhibitionForm()
    print(request.POST)
    if request.method == 'POST':
        form = OutdoorExhibitionForm(request.POST)  
        if form.is_valid():  
            form.save()  
        else:
            print("ERROR")


    return render(request, 'web_app/teacher/student_selection.html', {'form': form , 'id' : 2})   


def editor_prototype(request):
    template = loader.get_template('web_app/editor/editor.html')
    demo = VR_Templates.objects.filter(id=7).values()
    temp = demo[0]['basis']
    context = {
		'title1': "Teacher Dashboard",
		'header_content': 'Index header content',
        'basis': temp
	}   

    
    return HttpResponse(template.render(context, request)) 


def display403(request):
    template = loader.get_template('web_app/errors/403.html')
    context = {
		'title': "Student Selection",
		'header_content': 'Index header content',
	}   

    
    return HttpResponse(template.render(context, request)) 


def student_dashboard(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, stu, decoded = at.authenticateStudent(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( stu == False):
        return HttpResponseRedirect('/web_app/teacher/dashboard/')
        
    template = loader.get_template('web_app/student/dashboard.html')
    context = {
		'title': "Student Dashboard",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_num': 3,
        'art_num': 5
	}   

    return HttpResponse(template.render(context, request))


def student_artworks(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, stu, decoded = at.authenticateStudent(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( stu == False):
        return HttpResponseRedirect('/web_app/teacher/dashboard/')
        
    template = loader.get_template('web_app/student/myartworks.html')
    context = {
		'title': "My Artworks",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_num': 3,
        'art_num': 5
	}   

    return HttpResponse(template.render(context, request))


def student_exhibitions(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, stu, decoded = at.authenticateStudent(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( stu == False):
        return HttpResponseRedirect('/web_app/teacher/dashboard/')
        
    template = loader.get_template('web_app/student/myexhibitions.html')
    context = {
		'title': "My Exhibitions",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_num': 3,
        'art_num': 5
	}   

    return HttpResponse(template.render(context, request))


def createAr(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, stu, decoded = at.authenticateStudent(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( stu == False):
        return HttpResponseRedirect('/web_app/teacher/dashboard/')
        
    template = loader.get_template('web_app/ar-exhibitions/createAR.html')
    context = {
		'title': "Create AR Exhibition",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_title': 'Autumn',
        'teacher': 'Bob Ross'
	}   

    return HttpResponse(template.render(context, request))


def ar_display(request):
    template = loader.get_template('web_app/visitor/ar_display.html')
    context = {
		'title': "View AR Exhibition",
		'header_content': 'Index header content',
        'exh_title': 'Picasso Downtown',
        'teacher': 'Michalis Papadopoulos'
	}   

    return HttpResponse(template.render(context, request))


def logout(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay,decoded = at.authenticate(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    response = HttpResponseRedirect('/web_app/login/')
    response.delete_cookie('access_tkn')
    response.delete_cookie('refresh_tkn')
    return response


class getAllOutdoorExhibitions(RetrieveAPIView):
    """
    get: Get data of all outdoor exhibitions.
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'outdoor_exhibition'], 
    ]
    
    response_dict = build_fields('getAllOutdoorExhibitions', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get data of all outdoor exhibitions based.
        '''
        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = OutdoorExhibitionSerializer(data=req_data)
        
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                demo = OutdoorExhibition.objects.values()

                if not demo:
                    raise ApplicationError(['resource_not_found', 'outdoor_exhibition'])
            
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                header_data = {}
                header_data["exhibitions"] = []
                for outdoor in demo:
                    temp = {}
                    temp["id"] = outdoor['id']
                    temp["owner"] = outdoor['user_fk_id']
                    temp["start_date"] = outdoor['start_date']
                    temp["end_date"] = outdoor['end_date']
                    temp["description"] = outdoor['description']
                    temp["artworks"] = []
                    arts = OutdoorArtwork.objects.filter(exhibition_fk=outdoor['id']).values()
                    if not arts:
                        raise ApplicationError(['resource_not_found', 'outdoor exhibition artwork'])
                    for i in arts:
                        data = {}
                        data["lat"] = i['lat']
                        data["lon"] = i['lon']
                        demo2 = Artwork.objects.filter(id=i['artwork_fk_id']).values()
                        data["id"] = demo2[0]['id']
                        data["owner"] = demo2[0]['user_fk_id']
                        data["src"] = demo2[0]['src']
                        data["year"] = demo2[0]['year']
                        data["name"] = demo2[0]['name']
                        data["height"] = demo2[0]['height']
                        data["width"] = demo2[0]['width']
                        data["unit"] = demo2[0]['unit']
                        data["depth"] = demo2[0]['depth']
                        data["technique"] = demo2[0]['technique']
                        data["genre"] = demo2[0]['genre']
                        data["art_type"] = demo2[0]['art_type']
            
                        if not demo2:
                            raise ApplicationError(['resource_not_found', 'artwork'])
                        temp["artworks"].append(data)
                    header_data["exhibitions"].append(temp)
                        
                content[RESOURCE_OBJ] = header_data
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
            
        
        except Exception as e:
           log.error("{} Internal error: {}".format(request_details(request), str(e)))
           status_code, _ = get_code_and_response(['internal_server_error'])
           content = {
               MESSAGE: "Failed to fetch outdoor exhibition."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
    
    
class getAllOutdoorExhibitionsSorted(RetrieveAPIView):
    """
    get: Get data of all outdoor exhibitions sorted based on a latitude and longitude.
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'outdoor_exhibition'], 
    ]
    
    response_dict = build_fields('getAllOutdoorExhibitions', response_types)
    
    parameters = [openapi.Parameter(
        'lat',
        in_=openapi.IN_QUERY,
        description='The latitude of your position',
        type=openapi.TYPE_NUMBER,
        required=True,
    ),openapi.Parameter(
        'lon',
        in_=openapi.IN_QUERY,
        description='The longitude of your position',
        type=openapi.TYPE_NUMBER,
        required=True,
    )]
                  

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=parameters
    )
    
    def get(self, request, *args, **kwargs):
        '''
        Get data of all outdoor exhibitions based.
        '''
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = OutdoorExhibitionSerializer(data=req_data)
            lat = req_data.get('lat')
            lon = req_data.get('lon')
        
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                demo = OutdoorExhibition.objects.values()
                
                if not demo:
                    raise ApplicationError(['resource_not_found', 'outdoor_exhibition'])
            
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                header_data = {}
                header_data["exhibitions"] = []
                nearest_of_exhibition = {}
                cnt = 0
                for outdoor in demo:
                    arts = OutdoorArtwork.objects.filter(exhibition_fk=outdoor['id']).values()
                    if not arts:
                        raise ApplicationError(['resource_not_found', 'outdoor exhibition artwork'])
                    arts = sortGeo(arts,lat, lon)
                    nearest_of_exhibition[cnt] = [arts[0]['lat'],arts[0]['lon']]
                    cnt = cnt + 1 

                
                tmp_list = []
                for k, v in nearest_of_exhibition.items():      
                    temp_ins = []
                    temp_ins.append(v)
                    temp_ins.append(k)
                    tmp_list.append(temp_ins)                    
                
                nearest_of_exhibition = sorted(tmp_list, key=lambda x: geoDistance(lat,lon,x[0][0],x[0][1]))

                for point in nearest_of_exhibition:
                    pointer = point[1]
                    outdoor = demo[pointer]
                    temp = {}
                    temp["id"] = outdoor['id']
                    temp["owner"] = outdoor['user_fk_id']
                    temp["start_date"] = outdoor['start_date']
                    temp["end_date"] = outdoor['end_date']
                    temp["description"] = outdoor['description']
                    temp["artworks"] = []
                    arts = OutdoorArtwork.objects.filter(exhibition_fk=outdoor['id']).values()
                    if not arts:
                        raise ApplicationError(['resource_not_found', 'outdoor exhibition artwork'])
                   
                    for i in arts:
                        data = {}
                        data["lat"] = i['lat']
                        data["lon"] = i['lon']
                        demo2 = Artwork.objects.filter(id=i['artwork_fk_id']).values()
                        data["id"] = demo2[0]['id']
                        data["owner"] = demo2[0]['user_fk_id']
                        data["src"] = demo2[0]['src']
                        data["year"] = demo2[0]['year']
                        data["name"] = demo2[0]['name']
                        data["height"] = demo2[0]['height']
                        data["width"] = demo2[0]['width']
                        data["unit"] = demo2[0]['unit']
                        data["depth"] = demo2[0]['depth']
                        data["technique"] = demo2[0]['technique']
                        data["genre"] = demo2[0]['genre']
                        data["art_type"] = demo2[0]['art_type']
            
                        if not demo2:
                            raise ApplicationError(['resource_not_found', 'artwork'])
                        temp["artworks"].append(data)
                    header_data["exhibitions"].append(temp)
                    

                content[RESOURCE_OBJ] = header_data
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
            
        
        except Exception as e:
           log.error("{} Internal error: {}".format(request_details(request), str(e)))
           status_code, _ = get_code_and_response(['internal_server_error'])
           content = {
               MESSAGE: "Failed to fetch outdoor exhibition."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
  
    


class getAllOutdoorArtworksSorted(RetrieveAPIView):
    """
    get: Get data of all outdoor artworks sorted based on a latitude and longitude.
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'outdoor_exhibition'], 
    ]
    
    response_dict = build_fields('getAllOutdoorExhibitions', response_types)
    
    parameters = [openapi.Parameter(
        'lat',
        in_=openapi.IN_QUERY,
        description='The latitude of your position',
        type=openapi.TYPE_NUMBER,
        required=True,
    ),openapi.Parameter(
        'lon',
        in_=openapi.IN_QUERY,
        description='The longitude of your position',
        type=openapi.TYPE_NUMBER,
        required=True,
    )]
                  

    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters=parameters
    )
    
    def get(self, request):
        '''
        Get data of all outdoor artworks sorted based on a latitude and longitude. 
        '''
        #req_data = request.GET
        #lat = req_data.get('lat')
        #lon = req_data.get('lon')
        #art_list = OutdoorArtwork.objects.values()
        #art_list = sortGeo(art_list,lat,lon)
        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = UserSerializer(data=req_data)
            lat = req_data.get('lat')
            lon = req_data.get('lon')

            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                art_list = OutdoorArtwork.objects.values()
                
                if not art_list:
                    raise ApplicationError(['resource_not_found', 'artwork_list'])
                
                status_code, message = get_code_and_response(['success'])
                
                content = {}
                content[MESSAGE] = message
                header_data = {}
                header_data["artworks"] = []
                art_list = sortGeo(art_list,lat,lon)
                for a in art_list:
                    i = Artwork.objects.filter(id=a['artwork_fk_id']).values()[0]
                    data = {}
                    data["id"]          = a['id']
                    data["lat"]         = a['lat']
                    data["lon"]         = a['lon']
                    data["src"]         = i['src']
                    data["year"]        = i['year']
                    data["name"]        = i['name']
                    data["height"]      = i['height']
                    data["width"]       = i['width']
                    data["unit"]        = i['unit']
                    data["depth"]       = i['depth']
                    data["technique"]   = i['technique']
                    data["genre"]       = i['genre']
                    data["art_type"]    = i['art_type']
                    header_data["artworks"].append(data)
                    
                content[RESOURCE_OBJ] = header_data     
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response

            
        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to fetch artworks."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
  
    
class submitOutdoorArtwork(CreateAPIView):
    """
    post:
    Assigns an artwork to an outdoor exhibition
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = OutdoorArtworkSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    #permission_classes = (permissions.IsAuthenticated,)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('submitOutdoorArtwork', response_types)

    @swagger_auto_schema(
        responses=response_dict,
        #security=[{'Bearer': []}, ]
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))
        
        try:
            decoded = jwt.decode(
            request.COOKIES['access_tkn'],
            settings.SIMPLE_JWT['SIGNING_KEY'],
            settings.SIMPLE_JWT['ALGORITHM'],
            audience=settings.SIMPLE_JWT['AUDIENCE'])
            print(decoded)
                
        except Exception as e:
                log.error("{} Internal error: {}".format(request_details(request), str(e)))
                status_code, _ = get_code_and_response(['unauthorized'])
                content = {
                    MESSAGE: "Access token is invalid."
                }
                return Response(content, status=status_code)
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = OutdoorArtworkSerializer(data=req_data)

            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        form = OutdoorArtWorkForm(request.POST)
                        form.save()
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'outdoor artwork'
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to assign artwork."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])

    
class ExhibitionCreate(CreateAPIView):
    """
    post:
    Assigns a student to an exhibition.
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = ExhibitionSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('ExhibitionCreate', response_types)
    

    @swagger_auto_schema(
        responses=response_dict,
    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))

        try:
                    
            access_tkn = request.COOKIES.get('access_tkn')
            refresh_tkn = request.COOKIES.get('refresh_tkn')
            if not access_tkn:
                raise Exception("No access token provided!")

            tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
            if( tkn_okay == False):
                raise Exception("Access token invalid!")

            if( instr == False):
                raise Exception("User account unauthorized!")
            
        except Exception as e:
                log.error("{} Internal error: {}".format(request_details(request), str(e)))
                status_code, _ = get_code_and_response(['unauthorized'])
                content = {
                    MESSAGE: "Access token is invalid."
                }
                return Response(content, status=status_code)
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = ExhibitionSerializer(data=req_data)
            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        post = request.POST.copy() # to make it mutable
                        post['instructor_fk'] = decoded['user_id']
                        post['status'] = ExhibitionStatus.TemporaryStored
                        form = ExhibitionForm(post, request.FILES)
                        form.save()
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'exhibition assignment'
                        content[RESOURCE_ID] = Exhibition.objects.last().id
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response
                   

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to create exhibition assignment."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class AssignExhibition(CreateAPIView):
    """
    post:
    Creates an exhibition assignment
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = AssignStudentSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AssignExhibition', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,

    )
    def post(self, request, *args, **kwargs):
        log.debug("{} Received request".format(request_details(request)))

        try:
                    
            access_tkn = request.COOKIES.get('access_tkn')
            refresh_tkn = request.COOKIES.get('refresh_tkn')
            if not access_tkn:
                raise Exception("No access token provided!")

            tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
            if( tkn_okay == False):
                raise Exception("Access token invalid!")

            if( instr == False):
                raise Exception("User account unauthorized!")
            
        except Exception as e:
                log.error("{} Internal error: {}".format(request_details(request), str(e)))
                status_code, _ = get_code_and_response(['unauthorized'])
                content = {
                    MESSAGE: "Access token is invalid."
                }
                return Response(content, status=status_code)
        try:
            response = {}
            data = {}
            req_data = request.data
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = AssignStudentSerializer(data=req_data)
            
            if not serialized_item.is_valid():
                log.debug("{} VALIDATION ERROR: {}".format(
                        request_details(request),
                        serialized_item.formatted_error_response()
                    )
                )
                response = {}
                response[CONTENT] = serialized_item.formatted_error_response(include_already_exists=True)
                response[STATUS_CODE] = status.HTTP_400_BAD_REQUEST
                data = response
            else:
                with transaction.atomic():
                    try:
                        log.debug("{} VALID DATA".format(request_details(request)))
                        student = req_data.get('student_fk')
                        exhibition = req_data.get('assignment_fk')
                        assign = AssignedExhibitionStudents(
                            student_fk_id=student,
                            assignment_fk_id=exhibition,
                        )
                        assign.save()
                        changeExhibitionState(exhibition,ExhibitionStatus.AcceptingArtworks)
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'exhibition assignment'
                        response = {}
                        response[CONTENT] = content
                        response[STATUS_CODE] = status_code
                        log.debug("{} SUCCESS".format(request_details(request)))
                        data = response
                    except ApplicationError as e:
                        log.info("{} ERROR: {}".format(request_details(request), str(e)))
                        response = {}
                        response[CONTENT] = e.get_response_body()
                        response[STATUS_CODE] = e.status_code
                        data = response
                   

        except Exception as e:
            log.error("{} Internal error: {}".format(request_details(request), str(e)))
            status_code, _ = get_code_and_response(['internal_server_error'])
            content = {
                MESSAGE: "Failed to create exhibition assignment."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


class getAllUsers(RetrieveAPIView):
    """
    get: Get all users in the database.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'user'], 
    ]
    
    response_dict = build_fields('getAllUsers', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get all users in the database.
        '''
        error_message = "ERROR!"
        try:
                    
            access_tkn = request.COOKIES.get('access_tkn')
            refresh_tkn = request.COOKIES.get('refresh_tkn')
            if not access_tkn:
                error_message = "No access token provided!"
                raise Exception("No access token provided!")

            tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
            if( tkn_okay == False):
                error_message = "Access token invalid!"
                raise Exception("Access token invalid!")

            if( instr == False):
                error_message = "User account unauthorized!"
                raise Exception("User account unauthorized!")
            
        except Exception as e:
                log.error("{} Internal error: {}".format(request_details(request), str(e)))
                status_code, _ = get_code_and_response(['unauthorized'])
                content = {
                    MESSAGE: error_message
                }
                return Response(content, status=status_code)
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = UserSerializer(data=req_data)
        
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                demo = ActiveUsers.objects.values()
                t_who = ActiveUsers.objects.filter(id=decoded['user_id']).values()[0]
                who = Users.objects.filter(id=t_who['user_fk_id']).values()[0]    

                if not demo:
                    raise ApplicationError(['resource_not_found', 'User'])
            
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                header_data = {}
                header_data["users"] = []
                for user in demo:
                    if(user['user_fk_id'] != decoded['user_id']):
                        real_user = Users.objects.filter(id=user['user_fk_id']).values()[0]      
                        if(real_user['organization'] == who['organization']):
                            temp = {}
                            temp["id"] = real_user['id']
                            temp["email"] = real_user['email']
                            temp["name"] = real_user['name']
                            temp["surname"] = real_user['surname']
                            temp["role"] = real_user['role']
                            temp["organization"] = real_user['organization']
                            temp["class_level"] = real_user['class_level']
                            header_data["users"].append(temp)
                        
                content[RESOURCE_OBJ] = header_data
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
            
        
        except Exception as e:
           log.error("{} Internal error: {}".format(request_details(request), str(e)))
           status_code, _ = get_code_and_response(['internal_server_error'])
           content = {
               MESSAGE: "Failed to fetch user."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
    

class getFilteredExhibitions(RetrieveAPIView):
    """
    get: Get all temporary stored exhibitions of an instructor in the database.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'user'], 
    ]
    
    response_dict = build_fields('getFilteredExhibitions', response_types)
    
    parameters = openapi.Parameter(
        'status',
        in_=openapi.IN_QUERY,
        description='The status of exhibitions you want to fetch.',
        type=openapi.TYPE_NUMBER,
        required=True,
    )
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
        manual_parameters = [parameters],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get all temporary stored exhibitions of an instructor in the database.
        '''
        error_message = "ERROR!"
        try:
                    
            access_tkn = request.COOKIES.get('access_tkn')
            refresh_tkn = request.COOKIES.get('refresh_tkn')
            if not access_tkn:
                error_message = "No access token provided!"
                raise Exception("No access token provided!")

            tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
            if( tkn_okay == False):
                error_message = "Access token invalid!"
                raise Exception("Access token invalid!")

            if( instr == False):
                error_message = "User account unauthorized!"
                raise Exception("User account unauthorized!")
            
        except Exception as e:
                log.error("{} Internal error: {}".format(request_details(request), str(e)))
                status_code, _ = get_code_and_response(['unauthorized'])
                content = {
                    MESSAGE: error_message
                }
                return Response(content, status=status_code)
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = UserSerializer(data=req_data)
            status_flag = req_data.get('status')
            
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                exh_list = Exhibition.objects.filter(instructor_fk_id=decoded['user_id'],status=status_flag).values()

                if not exh_list:
                    raise ApplicationError(['resource_not_found', 'exhibition'])
            
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                
            
                header_data = {}
                header_data["exhibition"] = []
                for ex in exh_list:
                    temp = {}
                    temp["id"] = ex['id']
                    temp["title"] = ex['exhibition_title']
                    temp["start_date"] = ex['start_date']
                    temp["end_date"] = ex['end_date']
                    temp["space"] = ex['space_assign']
                    temp["description"] = ex['message']
                    temp["src"] = ex['image']
                    temp["status"] = ex['status']
                    header_data["exhibition"].append(temp)
                    
                content[RESOURCE_OBJ] = header_data
                response = {}
                response[CONTENT] = content
                response[STATUS_CODE] = status_code
                log.debug("{} SUCCESS".format(request_details(request)))
                data = response
            except ApplicationError as e:
                log.info("{} ERROR: {}".format(request_details(request), str(e)))
                response = {}
                log.info("e.get_response_body(): {}".format(e.get_response_body()))
                log.info("e.status_code: {}".format(e.status_code))
                response[CONTENT] = e.get_response_body()
                response[STATUS_CODE] = e.status_code
                data = response
            
        
        except Exception as e:
           log.error("{} Internal error: {}".format(request_details(request), str(e)))
           status_code, _ = get_code_and_response(['internal_server_error'])
           content = {
               MESSAGE: "Failed to fetch exhibitions."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
  
  
from django.http.response import FileResponse
from django.http import HttpResponseForbidden

def media_access(request, path):    
    used_path = 'images/' + path
    access_granted,decoded = at.authenticate(request,settings)
    if access_granted == False:
        return HttpResponseForbidden('Not authorized to access this media. CHECK') 
    image = Artwork.objects.filter(src=used_path,user_fk_id=decoded['user_id']).values()
    used_path = 'media/images/' + path
    if (access_granted and len(image) > 0 ):
        img = open(used_path, 'rb')
        response = FileResponse(img)
        return response
    else:
        return HttpResponseForbidden('Not authorized to access this media. CHECK')      
