from .views import *

class getAllOutdoorArtworks(RetrieveAPIView):
    """
    get: Get data of all outdoor artworks.
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
    def get(self, request):
        '''
        Get data of all outdoor artworks.
        '''
        

        
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            serialized_item = UserSerializer(data=req_data)

            #authorize:
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
    
