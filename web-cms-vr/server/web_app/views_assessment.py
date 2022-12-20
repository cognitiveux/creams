from .views import * 


# Checked on status_codes     
class GeneralAssessmentCreate(CreateAPIView):
    """
    post:
    Creates a general assessment of a student exhibition.
    """
    authentication_classes = [JWTAuthentication]
    serializer_class = GeneralAssessmentSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    response_types = [
        ['success'],
        ['unauthorized'],
        ['bad_request'],
        ['method_not_allowed'],
        ['internal_server_error']
    ]
    response_dict = build_fields('GeneralAssessmentCreate', response_types)

    @swagger_auto_schema(
        responses=response_dict,
    )
    
    
    def post(self, request, *args, **kwargs):
        ''' Post:  Creates a general assessment of a student exhibition  '''
        
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
            serialized_item = GeneralAssessmentSerializer(data=req_data)

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
                        uniqueCheck = GeneralAssessment.objects.filter(instructor_fk_id=post['instructor_fk'],assignment_fk_id=post['assignment_fk'],student_fk_id=post['student_fk']).values()
                        if( len(uniqueCheck) == 1):
                            uniqueCheck = GeneralAssessment.objects.get(instructor_fk_id=post['instructor_fk'],assignment_fk_id=post['assignment_fk'],student_fk_id=post['student_fk'])
                            temp = post['assessement']
                            uniqueCheck.assessement = temp
                            uniqueCheck.save(update_fields=['assessement'])
                        else:
                            if(int(post['instructor_fk']) != int(decoded['user_id']) ):
                                status_code, _ = get_code_and_response(['unauthorized'])
                                content = {
                                    MESSAGE: "Access token is invalid."
                                }
                                return Response(content, status=status_code)
                            student = Users.objects.filter(id=post['student_fk']).values()[0]
                            if( student['role'] != "STUDENT"):
                                print("ERROR")
                                raise Exception("Not a valid student")
                            
                            exhibition = AssignedExhibitionStudents.objects.filter(id=post['assignment_fk'],student_fk_id=post['student_fk']).values()
                            if len(exhibition) == 0:
                                raise Exception("Not a valid student")
                            
                            exhibition = AssignedExhibitionInstructor.objects.filter(assignment_fk_id=post['assignment_fk'],instructor_fk_id=post['instructor_fk']).values()
                            if len(exhibition) == 0:
                                main = Exhibition.objects.filter(id=post['assignment_fk'],instructor_fk_id=post['instructor_fk']).values()
                                if len(main) == 0:
                                    raise Exception("Not a valid instructor")
                            
                            form = GeneralAssessmentForm(post)
                            form.save()
                        status_code, message = get_code_and_response(['success'])
                        content = {}
                        content[MESSAGE] = message
                        content[RESOURCE_NAME] = 'assessment'
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
                MESSAGE: "Failed to create assessment."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
