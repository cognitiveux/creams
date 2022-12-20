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
import os
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
import stat
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
    chechRole,
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
INSTRUCTOR = "INSTRUCTOR"
STUDENT = "STUDENT"

TASK_STATUS = "task_status"

ALREADY_EXISTS_FIELDS = "already_exists_fields"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
ERROR_DETAILS = "error_details"
MISSING_REQUIRED_FIELDS = "missing_required_fields"


#def index(request):
#	template = loader.get_template('web_app/index.html')
#	context = {
#		'title': "Index title",
#		'header_content': 'Index header content'
#	}
#	return HttpResponse(template.render(context, request))


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


def submit_artwork(request):
	template = loader.get_template('web_app/student/submit_artwork.html')
	context = {
		'title': "Submit an artwork",
		'header_content': 'Index header content'
	}
	return HttpResponse(template.render(context, request))



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
    
    assigned_id = request.GET.get('assign')
    cross = AssignedExhibitionStudents.objects.filter(assignment_fk_id =assigned_id ,student_fk_id =decoded['user_id']).values()
    print(cross)
    if not cross:
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    template = loader.get_template('web_app/ar-exhibitions/createAR.html')
    exh = Exhibition.objects.filter(id=assigned_id).values()[0]
    if not exh:
        return HttpResponseRedirect('/web_app/student/dashboard/')
    inst = Users.objects.filter(id=exh['instructor_fk_id']).values()[0]
    full_name = inst["name"] + " " + inst["surname"]
    titleExh = exh['exhibition_title']
    outdoor = OutdoorExhibition.objects.filter(exhibition_fk_id = exh['id'], user_fk_id =decoded['user_id']).values()
    if not outdoor:
        inModel = OutdoorExhibition(
        user_fk_id = decoded['user_id'],
        exhibition_fk_id = assigned_id)

        inModel.save()
        outdoor = OutdoorExhibition.objects.filter(exhibition_fk_id = exh['id'], user_fk_id =decoded['user_id']).values()
        
    outdoor = outdoor[0]
    context = {
		'title': "Create AR Exhibition",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_title': titleExh,
        'teacher': full_name,
        'exh_id': outdoor['id']
	}   

    return HttpResponse(template.render(context, request))

  
#Checked on status_codes   
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


#Checked on status_codes
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
                        if(chechRole(student,STUDENT) == False):
                            print("NOT A STUDENT")
                            raise Exception
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


#Checked on status_codes
class AssignAdvisory(CreateAPIView):
    """
    post:
    Creates an exhibition advisory to an instructor
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = AssignAdvisorSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('AssignAdvisory', response_types)
    
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
            serialized_item = AssignAdvisorSerializer(data=req_data)
            
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
                        instructor = req_data.get('instructor_fk')
                        if(chechRole(instructor,INSTRUCTOR) == False):
                            print("NOT AN INSTRUCTOR")
                            raise Exception
                        exhibition = req_data.get('assignment_fk')
                        assign = AssignedExhibitionInstructor(
                            instructor_fk_id=instructor,
                            assignment_fk_id=exhibition,
                        )
                        assign.save()
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'exhibition advisory assignment'
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
                MESSAGE: "Failed to create exhibition advisory assignment."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])


#Checked on status_codes
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
  
    
# Checked on status_codes 
class getFilteredExhibitions(RetrieveAPIView):
    """
    get: Get all temporary stored exhibitions of an instructor in the database.
    """
    serializer_class = FilterExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getFilteredExhibitions', response_types)
    
    parameters = openapi.Parameter(
        'status',
        in_=openapi.IN_QUERY,
        description='The status of exhibitions you want to fetch.',
        type=openapi.TYPE_STRING,
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
            serialized_item = FilterExhibitionSerializer(data=req_data)
            status_flag = req_data.get('status')
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
                try:
                    log.debug("{} VALID DATA".format(request_details(request)))
                    exh_list = Exhibition.objects.filter(instructor_fk_id=decoded['user_id'],status=status_flag).values()
                    exh_list2 = AssignedExhibitionInstructor.objects.filter(instructor_fk_id=decoded["user_id"]).values()
                    
                    status_code, message = get_code_and_response(['success'])
                    content = {}
                    content[MESSAGE] = message
                    
                
                    header_data = {}
                    header_data["exhibitions"] = []
                    for ex in exh_list:
                        temp = {}
                        temp["id"] = ex['id']
                        temp["title"] = ex['exhibition_title']
                        temp["start_date"] = ex['start_date']
                        temp["end_date"] = ex['end_date']
                        temp["space"] = ex['space_assign']
                        temp["description"] = ex['message']
                        temp["thumbnail"] = ex['image']
                        temp["status"] = ex['status']
                        listStuds = AssignedExhibitionStudents.objects.filter(assignment_fk_id=ex['id']).values()
                        temp["participants"] = len(listStuds)
                        header_data["exhibitions"].append(temp)
                        
                    for indoor2 in exh_list2:
                        indoor = Exhibition.objects.filter(id=indoor2["assignment_fk_id"],status=status_flag).values()
                        if(len(indoor) == 1):
                            indoor = indoor[0]
                            temp = {}
                            temp["id"] = indoor['id']
                            temp["title"] = indoor['exhibition_title']
                            temp["start_date"] = indoor['start_date']
                            temp["end_date"] = indoor['end_date']
                            temp["description"] = indoor['message']
                            temp["thumbnail"] = indoor['image']
                            temp["status"] = indoor['status']
                            temp["thumbnail"] = indoor['image']
                            listStuds = AssignedExhibitionStudents.objects.filter(assignment_fk_id=indoor['id']).values()
                            temp["participants"] = len(listStuds)
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
               MESSAGE: "Failed to fetch exhibitions."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
  

def editor(request):
    template = loader.get_template('web_app/editor/editor.html')
    
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
    
    assigned_id = request.GET.get('assign')
    try:
        temp_id = request.GET.get('temp')
        if not temp_id:
            raise Exception
        crass = VR_Templates.objects.filter(id =temp_id ).values()
        if not crass:
            return HttpResponseRedirect('/web_app/teacher/dashboard/')
        
        demo = VR_Templates.objects.filter(id=temp_id).values()
        temp = demo[0]['basis']
        filename = temp[1:len(temp)]
        payload = open(filename, "r").read()
        
        context = {
		    'title': "VR Editor",
		    'header_content': 'Index header content',
            'userID': decoded['user_id'],
            'email': decoded['sub'],
            'name': decoded['name'],
            'surname': decoded['surname'],
            'organization': decoded['organization'],
            'role': decoded['role'],
            'basis': payload,
            'exh_id': request.GET.get('assign'),
            'temp_id': request.GET.get('temp'),
            'script': ' ',
            'reloaded' : 0
	    }   
    except Exception:
        ready = VR_Exhibition.objects.filter(exhibition_fk_id=assigned_id,student_fk_id =decoded['user_id']).values()
        if not ready:
            return HttpResponseRedirect('/web_app/teacher/dashboard/')
        
        name = "media/" + ready[0]['vr_exhibition']
        payload = open(name, "r").read()
        
        try:
            name = "media/" + ready[0]['vr_script']
            ac = open(name, "r").read()
        except Exception:
            ac = ' '

        context = {
		    'title': "VR Editor",
		    'header_content': 'Index header content',
            'userID': decoded['user_id'],
            'email': decoded['sub'],
            'name': decoded['name'],
            'surname': decoded['surname'],
            'organization': decoded['organization'],
            'role': decoded['role'],
            'basis': payload ,
            'exh_id': assigned_id,
            'temp_id': 0,
            'x_script' : ac,
            'reloaded' : 1
	    }   
        
        
    cross = AssignedExhibitionStudents.objects.filter(assignment_fk_id =assigned_id ,student_fk_id =decoded['user_id']).values()
    if not cross:
        return HttpResponseRedirect('/web_app/teacher/dashboard/')
    

    
    return HttpResponse(template.render(context, request)) 


def templateSelectionPage(request):
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
    
    assigned_id = request.GET.get('assign')
    cross = AssignedExhibitionStudents.objects.filter(assignment_fk_id =assigned_id ,student_fk_id =decoded['user_id']).values()
    print(cross)
    if not cross:
        return HttpResponseRedirect('/web_app/teacher/dashboard/')
    
    crass = VR_Exhibition.objects.filter(exhibition_fk_id=assigned_id,student_fk_id =decoded['user_id']).values()
    if  len(crass) > 0 :
        return HttpResponseRedirect('/web_app/student/editor/?assign=' + assigned_id)
    
    template = loader.get_template('web_app/student/templateSelection.html')
    exh = Exhibition.objects.filter(id=assigned_id).values()[0]
    inst = Users.objects.filter(id=exh['instructor_fk_id']).values()[0]
    full_name = inst["name"] + " " + inst["surname"]
    titleExh = exh['exhibition_title']
    sp_type = exh['space_assign']
    context = {
		'title': "Template Selection",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_id': assigned_id,
        'instructor': full_name,
        'exhibition_title': titleExh,
        'space':  sp_type
	}   
    
    return HttpResponse(template.render(context, request)) 


# Checked on status_codes 
class createVR(CreateAPIView):
    """
    post:
    Creates a new vr exhibition instance
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = VRCreateSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('createVR', response_types)

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

            tkn_okay, stud, decoded = at.authenticateStudent(request,settings)
            if( tkn_okay == False):
                raise Exception("Access token invalid!")

            if( stud == False):
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
            serialized_item = VRCreateSerializer(data=req_data)

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
                        print(request.POST)
                        post = request.POST.copy() # to make it mutable
                        post['student_fk'] = decoded['user_id']
                        try:
                            test = VR_Exhibition.objects.get(student_fk_id= decoded['user_id'], exhibition_fk_id=post['exhibition_fk'])
                            pathToDelete = "/code/media/" + str(test.vr_exhibition)
                            os.remove(pathToDelete)
                            try:
                                print("DELETE SCRIPT")
                                pathToDelete = "/code/media/" + str(test.vr_script)
                                os.remove(pathToDelete)
                                test.vr_script = request.FILES['vr_script']
                                test.save(update_fields=['vr_script'])
                            except Exception:
                                pass
                                
                            test.vr_exhibition = request.FILES['vr_exhibition']
                            test.save(update_fields=['vr_exhibition'])
                        except Exception:
                            form = VRExhibitionForm(post, request.FILES)
                            form.save()
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'vr_exhibition'
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
                MESSAGE: "Failed to create VR exhibition."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
    