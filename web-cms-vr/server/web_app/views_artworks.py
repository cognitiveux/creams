from .views import *

# Checked on status_codes
class getAllOutdoorArtworks(RetrieveAPIView):
    """
    get: Get data of all outdoor artworks assigned to an outdoor exhibition.
    """
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'], #MISSING IN STATUS CODES
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getAllOutdoorArtworks', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request):
        '''
        Get data of all outdoor artworks assigned to an outdoor exhibition.
        '''
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))

            #authorize:
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                art_list = OutdoorArtwork.objects.values()
                
                status_code, message = get_code_and_response(['success'])
                
                content = {}
                content[MESSAGE] = message
                header_data = {}
                header_data["artworks"] = []
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
   
# Checked on status_codes 
class getStudentsArtworks(RetrieveAPIView):
    """
    get: Get data all artworks of a student based on their jwt token.
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
    ]
    
    response_dict = build_fields('getStudentsArtworks', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
    )

    def get(self, request):
        '''
        Get data all artworks of a student based on their jwt token.
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
     
# Checked on status_codes. 
class getArtwork(RetrieveAPIView):
    """
    get: Get data of an artwork based on its id.
    """
    serializer_class = ArtworkSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'], # MISSING ON DESCRIPTION
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
  
# Checked on status_codes
class ArtworkCreate(CreateAPIView):
    """
    post:
    Creates a new artwork instance
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = ArtworkCreateSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'], # MISSING ON DESCRIPTION
        ['unsupported_media_type'],
        ['internal_server_error']
    ]
    response_dict = build_fields('ArtworkCreate', response_types)

    @swagger_auto_schema(
        responses=response_dict,
    )
    
    
    def post(self, request, *args, **kwargs):
        ''' Post:  Creates a new artwork instance  '''
        
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
                        post = request.POST.copy() # to make it mutable
                        post['user_fk'] = decoded['user_id']
                        form = ArtWorkForm(post, request.FILES)
                        t = form.save()
                        art = Artwork.objects.filter(id=t.id).values()[0]
                        path_of_image = "/code/media/" + art['src']
                        os.chmod(path_of_image , stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
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

# Checked on status_codes
class getAllOutdoorArtworksSorted(RetrieveAPIView):
    """
    get: Get data of all outdoor artworks sorted based on a latitude and longitude.
    """
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'], # MISSING IN STATUS CODES
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getAllOutdoorArtworksSorted', response_types)
    
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
            lat = req_data.get('lat')
            lon = req_data.get('lon')

            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                art_list = OutdoorArtwork.objects.values()
                
                
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
  