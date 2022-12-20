# Serializers define the API representation.
from django.contrib.auth.hashers import check_password
from django.utils.six import text_type
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

import datetime

from .application_error import ApplicationError
from .logging import logger as log
from .models import *
from .status_codes import (
    get_code_and_response,
)


ALREADY_EXISTS_FIELDS = "already_exists_fields"
BAD_FORMATTED_FIELDS = "bad_formatted_fields"
ERROR_DETAILS = "error_details"
MESSAGE = "message"
MISSING_REQUIRED_FIELDS = "missing_required_fields"
UNIQUE = "unique"
DJANGO_VALIDATION_ERROR_CODES = [
    "invalid",
    "invalid_choice",
    "min_length",
    "min_value",
    "max_length",
    "max_value",
]


def formatted_error_response_empty_params(validation_error):
    response = {
        ALREADY_EXISTS_FIELDS: [],
        BAD_FORMATTED_FIELDS: [],
        MISSING_REQUIRED_FIELDS: []
    }
    response[MESSAGE] = validation_error.__repr__()
    return response


class CustomSerializer(serializers.ModelSerializer):
    """
    A custom class to implement a way to return any validation errors
    in the desired format
    """
    def formatted_error_response(self, include_already_exists=False):
        """
        Returns (dict):
            A dictionary with the errors when a status code 400 bad request has occured
        """
        error_details_dict = {}
        response = {
            ALREADY_EXISTS_FIELDS: [],
            BAD_FORMATTED_FIELDS: [],
            MISSING_REQUIRED_FIELDS: []
        }
        append_bad_request_msg = False

        for field in self._errors:
            if self._errors[field][0].code == UNIQUE:
                response[ALREADY_EXISTS_FIELDS].append(field)

            elif self._errors[field][0].code in DJANGO_VALIDATION_ERROR_CODES:
                response[BAD_FORMATTED_FIELDS].append(field)
            else:
                response[MISSING_REQUIRED_FIELDS].append(field)

            # Add descriptive error messages
            error_details_dict[field] = []

            for item in self._errors[field]:
                error_details_dict[field].append(item)

        if not include_already_exists:
            response.pop(ALREADY_EXISTS_FIELDS)

        response[ERROR_DETAILS] = error_details_dict

        return response


class AccountMgmtLoginSerializer(TokenObtainPairSerializer):
    """
    The serializer for creating a JWT
    """

    def __init__(self, *args, **kwargs):
        super(AccountMgmtLoginSerializer, self).__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField(max_length=50, source='Users.email')
        self.fields['password'] = serializers.CharField(max_length=500, source='Users.password')

    @classmethod
    def get_token(cls, user):
        """
        Returns:
            The generated JWT
        """
        token = super(AccountMgmtLoginSerializer, cls).get_token(user)
        email = user.email
        user_row = Users.objects.filter(email=email).values('role', 'organization', 'name', 'surname')
       
        user_row_name = user_row[0].get('name')
        user_row_surname = user_row[0].get('surname')
        user_row_organization = user_row[0].get('organization')
        user_row_role = user_row[0].get('role')

        # Create custom JWT
        token['iss'] = "CreamsAuthentication"
        token['iat'] = int(str(datetime.datetime.now().timestamp()).split('.')[0])
        token['sub'] = email
        token['name'] = user_row_name
        token['surname'] = user_row_surname
        token['organization'] = user_row_organization
        token['role'] = user_row_role

        return token

    def validate(self, attrs):
        '''
        Validation for JSON Web Token creation.

        Returns:
            status_code, response_body
        '''
        user = None
        self.response_body = {}
        bad_formatted_fields = []
        missing_required_fields = []
        already_exists_fields = []
        error_details_dict = {}

        for field_name in self.fields:
            try:
                self.fields[field_name].run_validation(attrs.get(field_name))
            except serializers.ValidationError as e:
                # treat blank as missing field
                if e.detail[0].code == 'blank' or e.detail[0].code == 'null':
                    missing_required_fields.append(field_name)
                else:
                    bad_formatted_fields.append(field_name)

                if field_name not in error_details_dict:
                    error_details_dict[field_name] = []

                error_details_dict[field_name].append(e.__repr__())

        # Check for bad formatted fields
        if len(bad_formatted_fields) > 0 or len(missing_required_fields) > 0:
            log.debug("[AccountMgmtLoginSerializer] [validate] Bad formatted fields")
            self.response_body[MISSING_REQUIRED_FIELDS] = missing_required_fields
            self.response_body[BAD_FORMATTED_FIELDS] = bad_formatted_fields
            self.response_body[ALREADY_EXISTS_FIELDS] = already_exists_fields
            self.response_body[ERROR_DETAILS] = error_details_dict
            status, message = get_code_and_response(['bad_request'])
            self.response_body[MESSAGE] = message
            return status, self.response_body

        email = attrs.get('email')
        password = attrs.get('password')
        user_row = Users.objects.filter(email=email).first()

        # Check if user does not exist and return appropriate error code
        if not user_row:
            log.debug("[AccountMgmtLoginSerializer] [validate] User not found")
            raise ApplicationError(['resource_not_found', 'user'])

        user_fk_id = user_row.id
        active_user_row = ActiveUsers.objects.filter(user_fk_id=user_fk_id).first()

        if not active_user_row:
            raise ApplicationError(['resource_not_activated', 'user'])

        if not active_user_row.ts_activation:
            raise ApplicationError(['resource_not_activated', 'user'])

        if user_row.check_password(password):
            log.info("[AccountMgmtLoginSerializer] [validate] Valid credentials")
            refresh = self.get_token(user_row)
            status_code, message = get_code_and_response(['resource_created_return_obj', 'jwt'])
            self.response_body[MESSAGE] = message
            self.response_body['resource_name'] = 'jwt'
            tokens = {
                'access': text_type(refresh.access_token),
                'refresh': text_type(refresh)
            }
            self.response_body['resource_obj'] = tokens
            return status_code, self.response_body
        else:
            log.info("[AccountMgmtLoginSerializer] [validate] Invalid credentials")
            raise ApplicationError(['unauthorized'])

    def formatted_error_response(self):
        '''
        Returns:
            The response body produced by the validate function
        '''
        return self.response_body


class AccountMgmtActivateAccountSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')

    class Meta:
        model = ActiveUsers
        fields = ('email', 'verification_code')
        extra_kwargs = {
            'email': {
                'required': True
            },
            'verification_code': {
                'required': True
            }
        }


class AccountMgmtCreateUserSerializer(CustomSerializer):

    class Meta:
        model = Users
        fields = ('email', 'name', 'organization', 'password', 'role', 'surname', 'class_level')
        extra_kwargs = {
            'email': {
                'required': True
            },
            'name': {
                'required': True
            },
            'organization': {
                'required': True
            },
            'password': {
                'required': True
            },
            'role': {
                'required': True
            },
            'surname': {
                'required': True
            },
            'class_level': {
                'required': True
            },
        }


class AccountMgmtPollResetEmailStatusSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')

    class Meta:
        model = Users
        fields = ('email',)
        extra_kwargs = {
            'email': {
                'required': True
            },
        }


class AccountMgmtPollVerificationEmailStatusSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')

    class Meta:
        model = Users
        fields = ('email',)
        extra_kwargs = {
            'email': {
                'required': True
            },
        }


class AccountMgmtRequestAccountVerificationCodeSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')

    class Meta:
        model = Users
        fields = ('email',)
        extra_kwargs = {
            'email': {
                'required': True
            },
        }


class AccountMgmtRequestPasswordResetCodeSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')

    class Meta:
        model = Users
        fields = ('email',)
        extra_kwargs = {
            'email': {
                'required': True
            },
        }


class AccountMgmtResetPasswordSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')
    password = serializers.CharField(max_length=500, source='Users.password')

    class Meta:
        model = ResetPassword
        fields = ('email', 'password', 'reset_code')
        extra_kwargs = {
            'email': {
                'required': True
            },
            'password': {
                'required': True
            },
            'reset_code': {
                'required': True
            }
        }


class AccountMgmtUpdatePasswordSerializer(CustomSerializer):
    email = serializers.EmailField(max_length=50, source='Users.email')
    current_password = serializers.CharField(max_length=500, source='Users.password')
    new_password = serializers.CharField(max_length=500, source='Users.password')

    class Meta:
        model = Users
        fields = ('email', 'current_password', 'new_password')
        extra_kwargs = {
            'email': {
                'required': True
            },
            'current_password': {
                'required': True
            },
            'new_password': {
                'required': True
            }
        }


class AccountMgmtRefreshTokenSerializer(TokenRefreshSerializer):
    """
    The serializer for refreshing a JWT
    """
    def validate(self, attrs):
        '''
        Validation for refreshing JSON Web Token.

        Returns:
            status_code, response_body
        '''
        self.response_body = {}
        bad_formatted_fields = []
        missing_required_fields = []
        already_exists_fields = []
        error_details_dict = {}

        for field_name in self.fields:
            try:
                self.fields[field_name].run_validation(attrs.get(field_name))
            except serializers.ValidationError as e:
                # treat blank as missing field
                if e.detail[0].code == 'blank' or e.detail[0].code == 'null':
                    missing_required_fields.append(field_name)
                else:
                    bad_formatted_fields.append(field_name)

                if field_name not in error_details_dict:
                    error_details_dict[field_name] = []

                error_details_dict[field_name].append(e.__repr__())

        # Check for bad formatted fields
        if len(bad_formatted_fields) > 0 or len(missing_required_fields) > 0:
            log.debug("[AccountMgmtRefreshTokenSerializer] Bad formatted fields")
            self.response_body[MISSING_REQUIRED_FIELDS] = missing_required_fields
            self.response_body[BAD_FORMATTED_FIELDS] = bad_formatted_fields
            self.response_body[ALREADY_EXISTS_FIELDS] = already_exists_fields
            self.response_body[ERROR_DETAILS] = error_details_dict
            status,message = get_code_and_response(['bad_request'])
            self.response_body[MESSAGE] = message
            return status, self.response_body

        try:
            token = super(AccountMgmtRefreshTokenSerializer, self).validate(attrs)
            status_code, message = get_code_and_response(['resource_created_return_str', 'jwt'])
            self.response_body[MESSAGE] = message
            self.response_body['resource_name'] = 'jwt'
            self.response_body['resource_str'] = text_type(token.get('access'))
            return status_code, self.response_body
        except Exception as e:
            log.info("[AccountMgmtRefreshTokenSerializer] Error occurred during validation of JWT: {}".format(str(e)))
            status_code, message = get_code_and_response(['unauthorized'])
            message = str(e)
            self.response_body['message'] = message
            return status_code, self.response_body


class ArtworkCreateSerializer(CustomSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'
    
        
class UserSerializer(CustomSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class SampleAuthenticatedSerializer(CustomSerializer):
    class Meta:
        model = Users
        fields = ()


class GreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = '__all__'
 
        
class ArtworkSerializer(CustomSerializer):
    class Meta:
        model = Artwork
        fields = ('src', 'name', 'user_fk', 'year', 'height','width','depth','unit','technique','genre','art_type')
        extra_kwargs = {
            'src': {
                'required': True
            },
            'name': {
                'required': True
            },
            'user_fk': {
                'required': False
            },
            'year': {
                'required': True
            },
            'height': { 
                'required': True
            },
            'width': { 
                'required': True
            },
            'depth': { 
                'required': True
            },
            'unit': { 
                'required': True
            },
            'technique': { 
                'required': True
            },
            'genre': { 
                'required': True
            },
            'art_type': { 
                'required': True
            },
        }
        
class OutdoorExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutdoorExhibition
        fields = '__all__'


class OutdoorArtworkSerializer(CustomSerializer):
    class Meta:
        model = OutdoorArtwork
        fields = ('artwork_fk', 'exhibition_fk', 'lat', 'lon', 'description')
        extra_kwargs = {
            'artwork_fk': {
                'required': True
            },
            'exhibition_fk': {
                'required': True
            },
            'lat': {
                'required': True
            },
            'lon': {
                'required': True
            },
            'description': { 
                'required': False
            }
        }
    
       
class ExhibitionSerializer(CustomSerializer):
    class Meta:
        model = Exhibition
        fields = ('exhibition_title', 'start_date', 'end_date', 'instructor_fk', 'space_assign','message','image','status')
        extra_kwargs = {
            'exhibition_title': {
                'required': True
            },
            'start_date': {
                'required': True
            },
            'end_date': {
                'required': True
            },
            'instructor_fk': {
                'required': False
            },
            'space_assign': { 
                'required': True
            },
            'message': { 
                'required': False
            },
            'image': { 
                'required': True
            },
            'status': { 
                'required': False
            },
        }
        
        
class VRCreateSerializer(CustomSerializer):
    class Meta:
        model = VR_Exhibition
        fields = ('student_fk', 'exhibition_fk', 'vr_exhibition','vr_script')
        extra_kwargs = {
            'student_fk': {
                'required': False
            },
            'exhibition_fk': {
                'required': True
            },
            'vr_exhibition': {
                'required': True
            },
            'vr_script': {
                'required': False
            },
        }
        
        
class VR_TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VR_Templates
        fields = '__all__'
        
        
class AssignStudentSerializer(CustomSerializer):
    class Meta:
        model = AssignedExhibitionStudents
        fields = '__all__'
        
        
class AssignAdvisorSerializer(CustomSerializer):
    class Meta:
        model = AssignedExhibitionInstructor
        fields = '__all__'
        
        
class GeneralAssessmentSerializer(CustomSerializer):
    class Meta:
        model = GeneralAssessment
        fields = ('instructor_fk', 'assignment_fk', 'student_fk', 'assessement')
        extra_kwargs = {
            'instructor_fk': {
                'required': True
            },
            'assignment_fk': {
                'required': True
            },
            'student_fk': {
                'required': True
            },
            'assessement': {
                'required': True
            },
        }
    
class FilterExhibitionSerializer(CustomSerializer):
    status = serializers.ChoiceField(choices=ExhibitionStatus.STATUS_CHOICES)
    class Meta:
        model = Exhibition
        fields = ('status',)
        extra_kwargs = {
            'status': {
                'required': True
            },
        }