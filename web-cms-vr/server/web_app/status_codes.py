from rest_framework import serializers
from drf_yasg import openapi
from .logging import logger as log
from .models import *

"""
Dictionaries included in the module are useful when someone wants to modify the documentation of the responses
For modifying the possible responses of a view:
1.First modify the response_types list in your view class and add a list in the 2d list
that agrees with STATUS_CODES which lives in this file.
2.Then in VIEWS_DESCRIPTION find the key of this class(or add it) and add your status_code in the list
and also add your keys that you want to be returned with this status_code in the response body.
3.For adding a new description for a response field in the response body:
Add in GENERAL_DESCRIPTIONS the key name and the description of the key
Add in FIELD_TYPES the type of the field
3.1.If it has many possible values add in ENUM_VARIABLES all the possible values
"""


"""
RESOURCE_NAMES dict provides a list with all the possible resource names that are related with
keys starting with resource_* in STATUS_CODES dictionary
"""
RESOURCE_NAMES = {
    'c_register_task_id': "Celery task ID for registration",
    'c_reset_task_id': "Celery task ID for reset code",
    'expired_reset_code': "Expired reset code",
    'incorrect_reset_code': "Incorrect reset code",
    'jwt': "JSON Web Token",
    'not_requested_reset_code': "Not requested reset code",
    'password': "Password",
    'reset_code': "Reset code",
    'user': "User",
    'artwork': "Artwork",
    'assignment':"Assignment",
    'outdoor_exhibition': "OutdoorExhibition",
    'artwork_list': "List of artworks",
    'vr_template': "VR exhibition template",
    'exhibition':"Exhibition Assignment",
    'vr_exhibition':"VR Exhibition Assignment",
    'assessment' : "Assessment of an instructor"
    
}


"""
Different types of variables which can be returned in response
"""
RESPONSE_TYPES = {
    'bool': '\<Boolean\>',
    'float': '\<Float\>',
    'int': '\<Integer\>',
    'dict': '\<Dictionary\>',
    'array': '\<Array\>',
}

"""
Classnames for which the bad request dict should not be generated
"""
IGNORE_BAD_REQUEST = []


"""
Contains different possible responses with their status code and message
"""
STATUS_CODES = {
    'resource_is_activated': {
        'code': 200,
        'msg': "Success. Also returns whether {} is activated or not in `resource_is_activated`."
    },
    'success': {
        'code': 200,
        'msg': "Success"
    },
    'success_with_status_return': {
        'code': 200,
        'msg': "Success. The status is returned in `task_status`."
    },
    'resource_created_return_obj': {
        'code': 201,
        'msg': "{} has been created successfully. The value is returned in `resource_obj`."
    },
    'resource_created_return_str': {
        'code': 201,
        'msg': "{} has been created successfully. The value is returned in `resource_str`."
    },
    'bad_formatted_json': {
        'code': 400,
        'msg': "Json parse failed"
    },
    'bad_request': {
        'code': 400,
        'msg': "Bad request (Invalid data) - Any missing, already existing or bad formatted fields will be returned"
    },
    'unauthorized': {
        'code': 401,
        'msg': "Unauthorized - The request lacks valid authentication credentials."
    },
    'resource_not_activated': {
        'code': 403,
        'msg': "Forbidden. {} is not activated. You must activate it to proceed."
    },
    'resource_not_allowed': {
        'code': 403,
        'msg': "Forbidden. {} is not allowed to access this resource."
    },
    'resource_not_found': {
        'code': 404,
        'msg': "{} not found"
    },
    'method_not_allowed': {
        'code': 405,
        'msg': "Method not allowed"
    },
    'unsupported_media_type': {
        'code': 415,
        'msg': "Unsupported media type"
    },
    'resource_expired': {
        'code': 422,
        'msg': "{} has expired"
    },
    'resource_not_requested': {
        'code': 422,
        'msg': "{} not requested yet"
    },
    'resource_incorrect': {
        'code': 422,
        'msg': "{} is incorrect"
    },
    'resource_invalid':{
        'code':422,
        'msg':'{} is invalid'
    },
    'internal_server_error': {
        'code': 500,
        'msg': "Internal server error"
    },
}


"""
Responses that contain a message with a variable.
The type of the variable is described in the message
"""
VARIABLE_RESULTS = {
    'request_limit_exceeded': {
        'code': 422,
        'msg': "Request limit exceeded. Try again in %s minutes",
        'type': [RESPONSE_TYPES['int']],
    }
}


"""
Description of various keys that appear in the response body
"""
GENERAL_DESCRIPTIONS = {
    'already_exists_fields': "Any field that is unique and already exists, will be returned in the list",
    'bad_formatted_fields': "Any field that is not in the correct format will be returned in the list",
    'email': "The email of the individual",
    'error_details': "A dictionary that contains descriptive information " \
        "about the validation errors in the form of key-value pairs. " \
        "Each key is a string that corresponds to the problematic field " \
        "and the associated value is a list of strings that contains the error details. " \
        "If a JSON parse error occurred, there will be only one key named `json`.",
    'message': "A general message description",
    'missing_required_fields': "The missing required fields are returned as a list",
    'extra_details': "Extra details regarding the resource",
    'reason': "The reason behind this error message",
    'resource': "A value associated with that resource",
    'resource_is_activated': "True if resource is activated, False otherwise",
    'resource_array': "An array with all the available data",
    'resource_bool': "A boolean value associated with the name of the resource",
    'resource_dict': "A dictionary result with all the available data",
    'resource_name': "The name of the resource",
    'resource_id': "The id of the resource",
    'resource_obj': "A dictionary that contains the JWT " \
        "in the form of key-value pairs. " \
        "The key `access` is a string that corresponds to the JWT access token " \
        "and the key `refresh` is a string that corresponds to the JWT refresh token. ",
    'resource_str': "A string value associated with the resource_name",
    'task_status': "The status of the task: ['PENDING', 'SUCCESS', 'FAILURE']",
    'artwork' : "Data of an artwork",
    'outdoor_artwork' : "Data of an outdoor artwork",
    'outdoor_exhibition' : "Data of an outdoor exhibition",
    'outdoor_exhibitions' : "Data of outdoor exhibitions",
    'artwork_list' : "List of artworks",
    'vr_template' : "VR Exhibition template",
    'user' : "Data of an instructor or a student",
    'assignment' : "Student assignment to exhibition",
    'exhibition' : "Data of an exhibition",
    'exhibitions' : "List of exhibitions",
    'vr_exhibition' : "A Virtual Reality exhibition",
    'assessment' : "Assessment of an instructor"
} 

"""
Description for responses that need to be custom.
    key: classname
    value: the openapi dictionary specification for describing a response body
"""
CUSTOM_RESPONSES = {
    'getArtwork': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'id': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Artwork ID"
                        },
                        'name': {
                            'type': openapi.TYPE_STRING,
                            'description': "Artwork name"
                        },
                        'src': {
                            'type': openapi.TYPE_OBJECT,
                            'description': "Artwork source"
                        },
                        'year': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Artwork year of creation"
                        },
                        'owner': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Artwork owner"
                        },
                        'height': {
                            'type': openapi.TYPE_NUMBER,
                            'description': "Artwork height"
                        },
                        'width': {
                            'type': openapi.TYPE_NUMBER,
                            'description': "Artwork width"
                        },
                        'depth': {
                            'type': openapi.TYPE_NUMBER,
                            'description': "Artwork depth"
                        },
                        'unit': {
                            'type': openapi.TYPE_NUMBER,
                            'description': "Artwork unit"
                        },
                        'technique': {
                            'type': openapi.TYPE_STRING,
                            'description': "Artwork technique"
                        },
                        'genre': {
                            'type': openapi.TYPE_STRING,
                            'description': "Artwork genre"
                        },
                        'art_type': {
                            'type': openapi.TYPE_STRING,
                            'description': "Artwork type"
                        },
                    }
                }
            }
        }
    },       
    'getOutdoorExhibition': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'id': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Exhibition ID"
                        },
                        'title': {
                            'type': openapi.TYPE_STRING,
                            'description': "Exhibition ID"
                        },
                        'thumbnail': {
                            'type': openapi.TYPE_OBJECT,
                            'description': "Exhibition Thumbnail"
                        },
                        'owner': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Exhibition owner"
                        },
                        'owner_name': {
                            'type': openapi.TYPE_STRING,
                            'description': "Exhibition owner name"
                        },
                        'start_date': {
                            'type': openapi.TYPE_OBJECT,
                            'description': "Exhibition start-date"
                        },
                        'end_date': {
                            'type': openapi.TYPE_OBJECT,
                            'description': "Exhibition end-date"
                        },
                        'description': {
                            'type': openapi.TYPE_STRING,
                            'description': "Exhibition description"
                        },
                        'artworks' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('outdoor_artwork'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'lat': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork latitude"
                                    },
                                    'lon': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork longitude"
                                    },
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork ID"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork name"
                                    },
                                    'src': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Artwork source"
                                    },
                                    'year': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork year of creation"
                                    },
                                    'owner': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork owner"
                                    },
                                    'height': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork height"
                                    },
                                    'width': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork width"
                                    },
                                    'depth': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork depth"
                                    },
                                    'unit': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork unit"
                                    },
                                    'technique': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork technique"
                                    },
                                    'genre': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork genre"
                                    },
                                    'art_type': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork type"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getStudentsArtworks': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'artworks' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('outdoor_artwork'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'lat': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork latitude"
                                    },
                                    'lon': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork longitude"
                                    },
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork ID"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork name"
                                    },
                                    'src': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Artwork source"
                                    },
                                    'year': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork year of creation"
                                    },
                                    'height': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork height"
                                    },
                                    'width': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork width"
                                    },
                                    'depth': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork depth"
                                    },
                                    'unit': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork unit"
                                    },
                                    'technique': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork technique"
                                    },
                                    'genre': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork genre"
                                    },
                                    'art_type': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork type"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getFilteredExhibitions': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'exhibitions' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('exhibition'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition ID"
                                    },
                                    'title': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Title"
                                    },
                                    'start_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Start Date"
                                    },
                                    'end_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "End Date"
                                    },
                                    'space': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Space"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition Thumbnail"
                                    },
                                    'description': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Description"
                                    },
                                    'status': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Status"
                                    },
                                    'participants': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition participants count"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getIndoorExhibitions': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'exhibitions' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('exhibitions'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition ID"
                                    },
                                    'title': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Title"
                                    },
                                    'start_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Start Date"
                                    },
                                    'end_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "End Date"
                                    },
                                    'space': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Space"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition Thumbnail"
                                    },
                                    'description': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Description"
                                    },
                                    'status': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Status"
                                    },
                                    'participants': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition participants count"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getIndoorExhibitionsOfStudent': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'exhibitions' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('exhibitions'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition ID"
                                    },
                                    'title': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Title"
                                    },
                                    'instructor': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Instructors name"
                                    },
                                    'start_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Start Date"
                                    },
                                    'end_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "End Date"
                                    },
                                    'space': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Space"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition Thumbnail"
                                    },
                                    'description': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Description"
                                    },
                                    'status': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition Status"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getAllUsers': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'users' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('user'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "User ID"
                                    },
                                    'email': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User email"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User name"
                                    },
                                    'surname': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User surname"
                                    },
                                    'organization': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User organization"
                                    },
                                    'role': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User role"
                                    },
                                    'class_level': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User class or position"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getStudentsOfAnAssignment': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'students' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('user'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "User ID"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User name"
                                    },
                                    'surname': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "User surname"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getAllOutdoorArtworks': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'artworks' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('artwork_list'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'lat': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork latitude"
                                    },
                                    'lon': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork longitude"
                                    },
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork ID"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork name"
                                    },
                                    'src': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Artwork source"
                                    },
                                    'year': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork year of creation"
                                    },
                                    'height': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork height"
                                    },
                                    'width': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork width"
                                    },
                                    'depth': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork depth"
                                    },
                                    'unit': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork unit"
                                    },
                                    'technique': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork technique"
                                    },
                                    'genre': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork genre"
                                    },
                                    'art_type': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork type"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getAllOutdoorArtworksSorted': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'artworks' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('outdoor_artwork'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'lat': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork latitude"
                                    },
                                    'lon': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork longitude"
                                    },
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork ID"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork name"
                                    },
                                    'src': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Artwork source"
                                    },
                                    'year': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Artwork year of creation"
                                    },
                                    'height': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork height"
                                    },
                                    'width': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork width"
                                    },
                                    'depth': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork depth"
                                    },
                                    'unit': {
                                        'type': openapi.TYPE_NUMBER,
                                        'description': "Artwork unit"
                                    },
                                    'technique': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork technique"
                                    },
                                    'genre': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork genre"
                                    },
                                    'art_type': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Artwork type"
                                    },
                                }
                            }    
                        },
                    }
                },
            }
        },
    },
    'getVRTemplate' : {
                200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'id': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Template ID"
                        },
                        'basis': {
                            'type': openapi.TYPE_STRING,
                            'description': "Template"
                        },
                        'name': {
                            'type': openapi.TYPE_STRING,
                            'description': "Template Name"
                        },
                        'rooms': {
                            'type': openapi.TYPE_INTEGER,
                            'description': "Number of rooms in the exhibition"
                        },
                    }
                }
            }
        }    
    },
    'getAllVRTemplates' : {
                200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': { 
                        'templates' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('vr_template'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': {
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Template ID"
                                    },
                                    'basis': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Template"
                                    },
                                    'name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Template Name"
                                    },
                                    'rooms': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Number of rooms in the exhibition"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Thumbnail of the exhibition"
                                    },
                                }
                            }
                        }
                    },
                }
            }    
        }
    },
    'getAllOutdoorExhibitions': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': {
                        'exhibitions' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('exhibitions'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': { 
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition ID"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition Thumbnail"
                                    },
                                    'title': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition ID"
                                    },
                                    'owner': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition owner"
                                    },
                                    'owner_name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition owner name"
                                    },
                                    'start_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition start-date"
                                    },
                                    'end_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition end-date"
                                    },
                                    'description': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition description"
                                    },
                                    'artworks' : {
                                        'type': openapi.TYPE_ARRAY,
                                        'description': GENERAL_DESCRIPTIONS.get('artwork_list'),
                                        'items': {
                                            'type': openapi.TYPE_OBJECT,
                                            'properties': {
                                                'lat': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork latitude"
                                                },
                                                'lon': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork longitude"
                                                },
                                                'id': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork ID"
                                                },
                                                'name': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork name"
                                                },
                                                'src': {
                                                    'type': openapi.TYPE_OBJECT,
                                                    'description': "Artwork source"
                                                },
                                                'year': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork year of creation"
                                                },
                                                'owner': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork owner"
                                                },
                                                'height': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork height"
                                                },
                                                'width': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork width"
                                                },
                                                'depth': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork depth"
                                                },
                                                'unit': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork unit"
                                                },
                                                'technique': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork technique"
                                                },
                                                'genre': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork genre"
                                                },
                                                'art_type': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork type"
                                                },
                                            }
                                        }    
                                    },
                                }
                            }
                            
                        },
                    }
                },
            },
            }
    },
    'getAllIndoorExhibitions': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': {
                        'exhibitions' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('exhibitions'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': { 
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition ID"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition Thumbnail"
                                    },
                                    'title': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition ID"
                                    },
                                    'owner': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition owner"
                                    },
                                    'owner_name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition owner name"
                                    },
                                    'start_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition start-date"
                                    },
                                    'end_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition end-date"
                                    },
                                }
                            }
                            
                        },
                    }
                },
            },
            }
    },
    'getAllOutdoorExhibitionsSorted': {
        200: {
            'type': openapi.TYPE_OBJECT,
            'properties': {
                'message': {
                    'type': openapi.TYPE_STRING,
                    'description': GENERAL_DESCRIPTIONS.get('message')
                },
                'resource_obj':{
                    'type': openapi.TYPE_OBJECT,
                    'properties': {
                        'exhibitions' : {
                            'type': openapi.TYPE_ARRAY,
                            'description': GENERAL_DESCRIPTIONS.get('outdoor_exhibitions'),
                            'items': {
                                'type': openapi.TYPE_OBJECT,
                                'properties': { 
                                    'id': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition ID"
                                    },
                                    'title': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition ID"
                                    },
                                    'thumbnail': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition Thumbnail"
                                    },
                                    'owner': {
                                        'type': openapi.TYPE_INTEGER,
                                        'description': "Exhibition owner"
                                    },
                                    'owner_name': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition owner name"
                                    },
                                    'start_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition start-date"
                                    },
                                    'end_date': {
                                        'type': openapi.TYPE_OBJECT,
                                        'description': "Exhibition end-date"
                                    },
                                    'description': {
                                        'type': openapi.TYPE_STRING,
                                        'description': "Exhibition description"
                                    },
                                    'artworks' : {
                                        'type': openapi.TYPE_ARRAY,
                                        'description': GENERAL_DESCRIPTIONS.get('artwork_list'),
                                        'items': {
                                            'type': openapi.TYPE_OBJECT,
                                            'properties': {
                                                'lat': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork latitude"
                                                },
                                                'lon': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork longitude"
                                                },
                                                'id': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork ID"
                                                },
                                                'name': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork name"
                                                },
                                                'src': {
                                                    'type': openapi.TYPE_OBJECT,
                                                    'description': "Artwork source"
                                                },
                                                'year': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork year of creation"
                                                },
                                                'owner': {
                                                    'type': openapi.TYPE_INTEGER,
                                                    'description': "Artwork owner"
                                                },
                                                'height': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork height"
                                                },
                                                'width': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork width"
                                                },
                                                'depth': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork depth"
                                                },
                                                'unit': {
                                                    'type': openapi.TYPE_NUMBER,
                                                    'description': "Artwork unit"
                                                },
                                                'technique': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork technique"
                                                },
                                                'genre': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork genre"
                                                },
                                                'art_type': {
                                                    'type': openapi.TYPE_STRING,
                                                    'description': "Artwork type"
                                                },
                                            }
                                        }    
                                    },
                                }
                            }
                            
                        },
                    }
                },
            },
            }
    },
}

"""
Associates field name from VIEWS_DESCRIPTION dictionary with resource type
"""
FIELD_TYPES = {
    'already_exists_fields': openapi.TYPE_ARRAY,
    'bad_formatted_fields': openapi.TYPE_ARRAY,
    'error_details': openapi.TYPE_OBJECT,
    'extra_details': openapi.TYPE_STRING,
    'message': openapi.TYPE_STRING,
    'missing_required_fields': openapi.TYPE_ARRAY,
    'reason': openapi.TYPE_STRING,
    'resource': openapi.TYPE_STRING,
    'resource_array': openapi.TYPE_ARRAY,
    'resource_bool': openapi.TYPE_BOOLEAN,
    'resource_dict':openapi.TYPE_OBJECT,
    'resource_is_activated': openapi.TYPE_BOOLEAN,
    'resource_name': openapi.TYPE_STRING,
    'resource_obj': openapi.TYPE_OBJECT,
    'resource_str': openapi.TYPE_STRING,
    'resource_id': openapi.TYPE_INTEGER,
    'task_status': openapi.TYPE_STRING,
    'artwork' : openapi.TYPE_OBJECT,
    'outdoor_exhibition' : openapi.TYPE_OBJECT,
    'artwork_list': openapi.TYPE_OBJECT,
    'vr_template': openapi.TYPE_OBJECT,
    'user': openapi.TYPE_OBJECT,
    'assignment': openapi.TYPE_OBJECT,
    'exhibition': openapi.TYPE_OBJECT,
    'vr_exhibition': openapi.TYPE_OBJECT,
    'exhibitions': openapi.TYPE_OBJECT,
    'assessment' : openapi.TYPE_STRING
    
}


"""
Describes for each class it's enum variables and the values they can take
"""
ENUM_VARIABLES = {
    'AccountMgmtActivateAccount': {},
    'AccountMgmtCreateUser': {},
    'AccountMgmtLogin': {},
    'AccountMgmtPollResetEmailStatus': {
        'resource_name': ['user', 'c_reset_task_id'],
    },
    'AccountMgmtPollVerificationEmailStatus': {
        'resource_name': ['user', 'c_register_task_id'],
    },
    'AccountMgmtRefreshToken': {},
    'AccountMgmtRequestAccountVerificationCode': {},
    'AccountMgmtRequestPasswordResetCode': {},
    'AccountMgmtResetPassword': {
        'reason': [
            'expired_reset_code',
            'incorrect_reset_code',
            'not_requested_reset_code',
        ]
    },
    'AccountMgmtUpdatePassword': {},
    'ArtworkCreate': {},
    'SampleAuthenticated': {},
    'getArtwork':{},
    'getOutdoorExhibition':{},
    'getStudentsArtworks':{},
    'getVRTemplate':{},
    'getAllVRTemplates':{},
    'getAllOutdoorExhibitions':{},
    'getAllIndoorExhibitions':{},
    'getAllOutdoorExhibitionsSorted':{},
    'getAllOutdoorArtworks':{},
    'submitOutdoorArtwork':{},
    'getAllOutdoorArtworksSorted':{},
    'ExhibitionCreate':{},
    'getAllUsers':{},
    'AssignExhibition':{},
    'AssignAdvisory':{},
    'getFilteredExhibitions':{},
    'getIndoorExhibitions':{},
    'getIndoorExhibitionsOfStudent':{},
    'getStudentsOfAnAssignment':{},
    'createVR':{},
    'GeneralAssessmentCreate':{},
}


"""
Contains for each view the different status codes that can return and their corresponding
keys
"""
VIEWS_DESCRIPTION = {
    'AccountMgmtActivateAccount': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
                'resource_is_activated',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtCreateUser': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtLogin': [
        {
            'status_code': [201],
            'variables': [
                'message',
                'resource_name',
                'resource_obj',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
        {
            'status_code': [403, 404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
    ],
    'AccountMgmtPollResetEmailStatus': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'task_status'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtPollVerificationEmailStatus': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'task_status'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtRefreshToken': [
        {
            'status_code': [201],
            'variables': [
                'message',
                'resource_name',
                'resource_str'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'error_details'
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtRequestAccountVerificationCode': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
                'resource_is_activated',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404, 422],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtRequestPasswordResetCode': [
        {
            'status_code': [200, 403, 404, 422],
            'variables': [
                'message',
                'resource_name'
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtResetPassword': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [403, 404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [422],
            'variables': [
                'message',
                'resource_name',
                'reason'
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'AccountMgmtUpdatePassword': [
        {
            'status_code': [200, 422],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [403, 404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'ArtworkCreate': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'createVR': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'ExhibitionCreate': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
                'resource_id',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'submitOutdoorArtwork': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'SampleAuthenticated': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },
    ],
    'getArtwork' : [{
            'status_code': [200],
            'variables': [
                'message',
                'artwork',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],  
    'getOutdoorExhibition' : [{
            'status_code': [200],
            'variables': [
                'message',
                'outdoor_exhibition',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getStudentsArtworks' : [{
            'status_code': [200],
            'variables': [
                'message',
                'artwork_list',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllOutdoorArtworks' : [{
            'status_code': [200],
            'variables': [
                'message',
                'artwork_list',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllOutdoorArtworksSorted': [{
            'status_code': [200],
            'variables': [
                'message',
                'artwork_list',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getVRTemplate' : [{
            'status_code': [200],
            'variables': [
                'message',
                'vr_template',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllVRTemplates' : [{
            'status_code': [200],
            'variables': [
                'message',
                'vr_template',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllOutdoorExhibitions' : [{
            'status_code': [200],
            'variables': [
                'message',
                'artwork_list',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllOutdoorExhibitionsSorted' : [{
            'status_code': [200],
            'variables': [
                'message',
                'artwork_list',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllIndoorExhibitions' : [{
            'status_code': [200],
            'variables': [
                'message',
                'exhibitions',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [415, 500],
            'variables': [
                'message',
            ]
        },],
    'getAllUsers' : [{
            'status_code': [200],
            'variables': [
                'message',
                'user',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'AssignExhibition' : [{
            'status_code': [200],
            'variables': [
                'message',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'AssignAdvisory' : [{
            'status_code': [200],
            'variables': [
                'message',
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'getFilteredExhibitions' : [{
            'status_code': [200],
            'variables': [
                'message',
                'exhibition'
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'getIndoorExhibitions' : [{
            'status_code': [200],
            'variables': [
                'message',
                'exhibitions'
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'getIndoorExhibitionsOfStudent' : [{
            'status_code': [200],
            'variables': [
                'message',
                'exhibitions'
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'getStudentsOfAnAssignment' : [{
            'status_code': [200],
            'variables': [
                'message',
                'user'
                
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details'
            ],
        },
        {
            'status_code': [404],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [401, 415, 500],
            'variables': [
                'message',
            ]
        },],
    'GeneralAssessmentCreate': [
        {
            'status_code': [200],
            'variables': [
                'message',
                'resource_name',
            ]
        },
        {
            'status_code': [400],
            'variables': [
                'message',
                'bad_formatted_fields',
                'missing_required_fields',
                'already_exists_fields',
                'error_details',
            ]
        },
        {
            'status_code': [401,500],
            'variables': [
                'message',
            ]
        },
    ],
}


def _wrong_method_schema():
    """
    Returns:
        an openapi.Schema which corresponds to wrong method response
    """
    message_key = 'message'
    schema_dict = {
        'type':openapi.TYPE_OBJECT,
        'title':'Response body for status code 405',
        'description':'Following keys are returned as json',
        'properties':{
            message_key:{
                'type': FIELD_TYPES[message_key],
                'description': GENERAL_DESCRIPTIONS[message_key],
            },
        }
    }
    return openapi.Schema(**schema_dict)


def _bad_request_schema():
    '''
    Returns:
        openapi.Schema which corresponds to a bad request
    '''
    missing_required_fields = "missing_required_fields"
    already_exist_fields = "already_exist_fields"
    bad_formatted_fields = "bad_formatted_fields"
    error_details = "error_details"
    message_key = "message"
    schema_dict = {
        'type': openapi.TYPE_OBJECT,
        'title': "Response body for status code 400",
        'description': "Following keys are returned as json",
        'properties': {
            already_exist_fields: {
                'type': FIELD_TYPES[already_exist_fields],
                'description': GENERAL_DESCRIPTIONS[already_exist_fields],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            bad_formatted_fields: {
                'type': FIELD_TYPES[bad_formatted_fields],
                'description': GENERAL_DESCRIPTIONS[bad_formatted_fields],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            missing_required_fields: {
                'type': FIELD_TYPES[missing_required_fields],
                'description': GENERAL_DESCRIPTIONS[missing_required_fields],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            error_details: {
                'type': FIELD_TYPES[error_details],
                'description': GENERAL_DESCRIPTIONS[error_details],
                'items': {
                    'type': openapi.TYPE_STRING
                }
            },
            message_key: {
                'type': FIELD_TYPES[message_key],
                'description': GENERAL_DESCRIPTIONS[message_key],
            },
        }
    }
    return openapi.Schema(**schema_dict)


def build_response_dictionary(status_list, is_description=True):
    '''
    Builds the response dictionary from the list of tuples which will be used by
    swagger_auto_schema. The form of the tuples is:
    (status_codes_dictionary_key,resource_name,return type)
    resource_names and return type are necessary sometimes depending on the status_codes_dictionary_key

    Arguments:
        status_list (1d list): The list with correct keys according to the required format
    Raises:
        KeyNotFoundException if any key is not found in any dictionary
    '''
    response_dict = {}

    for status_item in status_list:
        code, msg = get_code_and_response(status_item, is_description)
        if code in response_dict.keys():
            response_dict[code] += ' or ' + msg
        else:
            response_dict[code] = msg

    return response_dict


def get_code_and_response(status_item,is_description=False):
    """
    Test

    Arguments:
        status_item (list): A list with size 1,2 or 3 with the appropriate keys according to
            STATUS_CODES defined in status_codes.py
            1st position of the list corresponds to the key of STATUS_CODES dict in status_codes py
            2nd position of the list corresponds to the resource_name and should be used with a key
            that starts with the prefix \'resource\'
            3rd position corresponds to another resource name which is somehow related
            with the resource_name in the 2nd position of the list
            Should be used only when 1st position of the dict is a key of the STATUS_CODES that is related with 2 resources
        is_description (bool):
            Whether the actual value of the variable should be present or the type of the variable.

    Returns:
        status_code,message according to the status_item contents

    """
    code = ''
    msg = ''

    if status_item[0] in STATUS_CODES.keys():
        if len(status_item)==1:
            msg = STATUS_CODES[status_item[0]]['msg']
        elif len(status_item)==2:
            msg = STATUS_CODES[status_item[0]]['msg'].format(RESOURCE_NAMES[status_item[1]])
        elif len(status_item)==3:
            msg = STATUS_CODES[status_item[0]]['msg'].format(RESOURCE_NAMES[status_item[1]],RESPONSE_TYPES[status_item[2]])
        code = STATUS_CODES[status_item[0]]['code']
    elif status_item[0] in VARIABLE_RESULTS.keys():
        if is_description:
            type_list = VARIABLE_RESULTS[status_item[0]]['type']
            msg = VARIABLE_RESULTS[status_item[0]]['msg']%(tuple(type_list))
        else:
            msg = VARIABLE_RESULTS[status_item[0]]['msg']%(tuple(status_item[1:]))
        code = VARIABLE_RESULTS[status_item[0]]['code']
    return code,msg


def build_fields(classname, status_keys):
    """Builds the dictionary which will be put as input to the swagger_auto_schema response.
    Keys will be of type (str) and will represent the status code and values will be of
    type rest_framework.response.Response.

    Args:
        classname (str):
            The classname of the caller
        status_keys (2d list):
            A 2d list where each sublist contains the keys specified in status_codes.STATUS_CODES & status_codes.RESOURCE_NAMES
            with their description

    Returns:
        A dict object where key is the status code and value is the openapi.Schema object
        If no keys are given in status_keys that correspond to 400 or 405 status codes then the function
        will autogenerate openapi.Schema objects for them.
    Raises:
        KeyNotFoundException if the status_keys given do not match with VIEWS_DESCRIPTION
        status codes of the given class.
    """
    status_text = build_response_dictionary(status_keys)
    response_dict = {}
    field_dict = {}
    for response_body in VIEWS_DESCRIPTION[classname]:
        property_dict = {}
        for variable_name in response_body['variables']:
            property_dict[variable_name] = {
                'type': FIELD_TYPES[variable_name],
                'description': GENERAL_DESCRIPTIONS[variable_name]
            }
            #check if there is a list of values allowed for this field
            if variable_name in ENUM_VARIABLES[classname]:
                property_dict[variable_name]['enum'] = ENUM_VARIABLES[classname][variable_name]
            if FIELD_TYPES[variable_name]==openapi.TYPE_ARRAY:
                property_dict[variable_name]['items'] = {
                    'type': openapi.TYPE_STRING
                }

        schema_dict = {
            'type': openapi.TYPE_OBJECT,
            'description': 'Following keys are returned as json'
        }

        for status_code in response_body['status_code']:
            schema_dict['title'] = 'Response body for status code {}'.format(status_code)

            #build the custom response and ignore the variable type
            if classname in CUSTOM_RESPONSES and status_code in CUSTOM_RESPONSES[classname]:
                schema_dict = CUSTOM_RESPONSES[classname][status_code]
            else:
                schema_dict['properties'] = property_dict

            response_dict[status_code] = openapi.Response(
                description=status_text[status_code],
                schema=openapi.Schema(**schema_dict)
            )

    # bad method status code
    response_dict[405] = openapi.Response(status_text[405],_wrong_method_schema())

    if classname not in IGNORE_BAD_REQUEST:
        #if no bad request case is specified, it has to be generated
        if 400 not in response_dict:
            response_dict[400] = openapi.Response(status_text[400],_bad_request_schema())

    #fill the remaining keys which do not have a documented response body with just their response text description
    for status_code in status_text.keys():
        if not status_code in response_dict.keys():
            response_dict[status_code]=status_text[status_code]

    return response_dict
