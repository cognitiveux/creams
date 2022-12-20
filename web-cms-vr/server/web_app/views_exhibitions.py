from .views import *


# Checked on status_codes     
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
    ]
    
    response_dict = build_fields('getAllOutdoorExhibitions', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get data of all outdoor exhibitions.
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

                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                header_data = {}
                header_data["exhibitions"] = []
                for outdoor in demo:
                    temp = {}
                    temp["id"] = outdoor['id']
                    temp["owner"] = outdoor['user_fk_id']
                    owner = Users.objects.filter(id=outdoor['user_fk_id']).values()[0]
                    temp["owner_name"] = owner['name'] + ' ' + owner['surname']
                    main = Exhibition.objects.filter(id=outdoor['exhibition_fk_id']).values()[0]
                    temp["thumbnail"] = main['image']
                    temp["start_date"] = main['start_date']
                    temp["end_date"] = main['end_date']
                    temp["title"] = main['exhibition_title']
                    temp["description"] = main['message']
                    temp["artworks"] = []
                    arts = OutdoorArtwork.objects.filter(exhibition_fk=outdoor['id']).values()
                    if not arts:
                        continue #REMEMBER: if an outdoor exhibition has no artworks it's not considered an exhibition
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
                        
                        # this could cause problems but it's unlikable
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
    
    
# Checked on status_codes     
class getAllIndoorExhibitions(RetrieveAPIView):
    """
    get: Get data of all indoor exhibitions. TO BE ONLY FOR PUBLISHED
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getAllIndoorExhibitions', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get data of all indoor exhibitions.
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
                demo = VR_Exhibition.objects.values()

            
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                header_data = {}
                header_data["exhibitions"] = []
                for indoor in demo:
                    temp = {}
                    temp["id"] = indoor['id']
                    temp["owner"] = indoor['student_fk_id']
                    owner = Users.objects.filter(id=indoor['student_fk_id']).values()[0]
                    temp["owner_name"] = owner['name'] + ' ' + owner['surname']
                    main = Exhibition.objects.filter(id=indoor['exhibition_fk_id']).values()[0]
                    temp["thumbnail"] = main['image']
                    temp["start_date"] = main['start_date']
                    temp["end_date"] = main['end_date']
                    temp["title"] = main['exhibition_title']
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
               MESSAGE: "Failed to fetch indoor exhibition."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])

    
# Checked on status_codes     
class getAllOutdoorExhibitionsSorted(RetrieveAPIView):
    """
    get: Get data of all outdoor exhibitions sorted based on a latitude and longitude.
    """
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        #['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getAllOutdoorExhibitionsSorted', response_types)
    
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
        import traceback
        '''
        Get data of all outdoor exhibitions sorted based on a latitude and longitude.
        '''
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            lat = float(req_data.get('lat'))
            lon = float(req_data.get('lon'))

            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                demo = OutdoorExhibition.objects.values()
                
                #if not demo:
                #    raise ApplicationError(['resource_not_found', 'outdoor_exhibitions'])
            
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
                        continue
                    #    raise ApplicationError(['resource_not_found', 'outdoor_artwork'])
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

                    owner = Users.objects.filter(id=outdoor['user_fk_id']).values()[0]
                    temp["owner_name"] = owner['name'] + ' ' + owner['surname']
                    main = Exhibition.objects.filter(id=outdoor['exhibition_fk_id']).values()[0]
                    temp["start_date"] = main['start_date']
                    temp["end_date"] = main['end_date']
                    temp["thumbnail"] = main['image']
                    temp["title"] = main['exhibition_title']
                    temp["description"] = main['message']
                    temp["artworks"] = []
                    arts = OutdoorArtwork.objects.filter(exhibition_fk=outdoor['id']).values()
                    #if not arts:
                    #    raise ApplicationError(['resource_not_found', 'outdoor_artwork'])
                   
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
            
                        #if not demo2:
                        #    raise ApplicationError(['resource_not_found', 'artwork'])
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
           print(traceback.print_exc())
           log.error("{} Internal error: {}".format(request_details(request), str(e)))
           status_code, _ = get_code_and_response(['internal_server_error'])
           content = {
               MESSAGE: "Failed to fetch outdoor exhibition."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])

  
# Checked on status_codes   
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
                    raise ApplicationError(['resource_not_found', 'outdoor_artwork'])
            
         
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                exhibition = demo[0]
                header_data = {}
                header_data["id"] = exhibition['id']
                header_data["owner"] = exhibition['user_fk_id']
                owner = Users.objects.filter(id=exhibition['user_fk_id']).values()[0]
                header_data["owner_name"] = owner['name'] + ' ' + owner['surname']
                main = Exhibition.objects.filter(id=exhibition['exhibition_fk_id']).values()[0]
                header_data["thumbnail"] = main['image']
                header_data["title"] = main['exhibition_title']
                header_data["start_date"] = main['start_date']
                header_data["end_date"] = main['end_date']
                header_data["description"] = main['message']
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

 
# Checked on status_codes   
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
        '''
        post: Assigns an artwork to an outdoor exhibition
        '''
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


# Checked on status_codes   
class getVRTemplate(RetrieveAPIView):
    """
    get: Get data of vr exhibition template.
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
        ['resource_not_found', 'vr_template'], 
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
 
 
# Checked on status_codes 
class getAllVRTemplates(RetrieveAPIView):
    """
    get: Get data of all vr exhibition templates.
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
    ]
    
    response_dict = build_fields('getAllVRTemplates', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )

    def get(self, request):
        '''
        Get data of all vr templates.
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
                demo = VR_Templates.objects.values()
                
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
                header_data = {}
                header_data["templates"] = []
                for temp in demo:
                    data = {}
                    data["id"] = temp['id']
                    data["basis"] = temp['basis']
                    data["name"] = temp['name']
                    data["rooms"] = temp['rooms']
                    data["thumbnail"] = temp['thumbnail']
                    header_data["templates"].append(data)
                
                response = {}
                content[RESOURCE_OBJ] = header_data
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
 

# Checked on status_codes
class getIndoorExhibitions(RetrieveAPIView):
    """
    get: Get data of all indoor exhibition assignments.
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getIndoorExhibitions', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get data of all indoor exhibitions assignments of an instructor.
        '''
        
        try:
            error_message = "ERROR!"
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
                    MESSAGE: error_message
                }
                return Response(content, status=status_code)
        
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = OutdoorExhibitionSerializer(data=req_data)
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                exh_list = Exhibition.objects.filter(instructor_fk_id=decoded["user_id"]).values()
                exh_list2 = AssignedExhibitionInstructor.objects.filter(instructor_fk_id=decoded["user_id"]).values()
                
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                header_data = {}
                header_data["exhibitions"] = []
                for indoor in exh_list:
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
                    
                for indoor2 in exh_list2:
                    indoor = Exhibition.objects.filter(id=indoor2["assignment_fk_id"]).values()[0]
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
               MESSAGE: "Failed to fetch exhibition assignments."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
    
    
# Checked on status_codes
class getIndoorExhibitionsOfStudent(RetrieveAPIView):
    """
    get: Get data of all indoor exhibition assignments of a student.
    """
    serializer_class = OutdoorExhibitionSerializer
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
    ]
    
    response_dict = build_fields('getIndoorExhibitionsOfStudent', response_types)
    
    @swagger_auto_schema(
        responses=response_dict,
        security=[],
    )
    def get(self, request, *args, **kwargs):
        '''
        Get data of all indoor exhibitions assignments of a student.
        '''
        
        try:
            error_message = "ERROR!"
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
                    MESSAGE: error_message
                }
                return Response(content, status=status_code)
        
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = OutdoorExhibitionSerializer(data=req_data)
            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                exh_list = AssignedExhibitionStudents.objects.filter(student_fk_id=decoded["user_id"]).values()
                
                status_code, message = get_code_and_response(['success'])
                content = {}
                content[MESSAGE] = message
            
                header_data = {}
                header_data["exhibitions"] = []
                for hand in exh_list:
                    indoor = Exhibition.objects.filter(id=hand['assignment_fk_id']).values()[0]
                    temp = {}
                    temp["id"] = indoor['id']
                    temp["title"] = indoor['exhibition_title']
                    temp["start_date"] = indoor['start_date']
                    temp["end_date"] = indoor['end_date']
                    temp["description"] = indoor['message']
                    teacher = Users.objects.filter(id=indoor['instructor_fk_id']).values()[0]
                    temp["instructor"] = teacher['name'] +  ' ' + teacher['surname'] 
                    temp["status"] = indoor['status']
                    temp["thumbnail"] = indoor['image']
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
               MESSAGE: "Failed to fetch exhibition assignments."
           }
           return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
