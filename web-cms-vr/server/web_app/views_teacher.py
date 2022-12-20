from .views import *
from django.http import HttpResponseNotAllowed

def teacher_dashboard(request):

    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    template = loader.get_template('web_app/teacher/dashboard.html')
    context = {
		'title': "Teacher Dashboard",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role']
	}   
        
    return HttpResponse(template.render(context, request))


def teacher_assessment(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    template = loader.get_template('web_app/teacher/assessment.html')
    context = {
		'title': "Assessment",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role']
	}   

    return HttpResponse(template.render(context, request))


def teacher_exhibition(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)

    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    template = loader.get_template('web_app/teacher/exhibition.html')
    context = {
		'title': "Initiate an exhibition",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'spaces' : [r[0] for r in ExhibitionSpaceModel.SPACE_CHOICES],
	}
    return HttpResponse(template.render(context, request))


def student_selection_by_teacher(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    valid_q = Exhibition.objects.filter(id=request.GET.get('q'), instructor_fk_id=decoded['user_id']).values()
    
    if(len(valid_q) == 0 ):
        url = reverse('display403')
        return HttpResponseRedirect(url)
    
    
    template = loader.get_template('web_app/teacher/student_selection.html')
    context = {
		'title': "Student Selection",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_id': request.GET.get('q')
	}   

    
    return HttpResponse(template.render(context, request)) 


def student_assessment_by_teacher(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    valid_q = Exhibition.objects.filter(id=request.GET.get('q')).values()
    if(len(valid_q) == 0 ):
        url = reverse('display403')
        return HttpResponseRedirect(url)
    
    valid_q = Exhibition.objects.filter(id=request.GET.get('q'),instructor_fk_id=decoded['user_id']).values()
    exh = Exhibition.objects.filter(id=request.GET.get('q')).values()[0]
    coadv = AssignedExhibitionInstructor.objects.filter(assignment_fk_id=exh["id"],instructor_fk_id=decoded['user_id']).values()
    if(len(valid_q) == 0 and len(coadv) == 0):
        url = reverse('display403')
        return HttpResponseRedirect(url)
    
    template = loader.get_template('web_app/teacher/assess_students.html')
    context = {
		'title': "Student Assessment",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'exh_id': request.GET.get('q')
	}   

    
    return HttpResponse(template.render(context, request)) 


def coadvisor_assessment(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    template = loader.get_template('web_app/teacher/assessment/coadvisor.html')
    context = {
		'title': "Coadvisor Assessment",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
	}   

    
    return HttpResponse(template.render(context, request)) 


def main_assessment(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    template = loader.get_template('web_app/teacher/assessment/main_advisor.html')
    context = {
		'title': "Student Assessment",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
	}   

    
    return HttpResponse(template.render(context, request)) 


# Checked on status_codes     
class getStudentsOfAnAssignment(RetrieveAPIView):
    """
    get: Get all students of an assignment.
    """
    permission_classes = (permissions.AllowAny,)
    response_types = [
        ['success'],
        ['bad_request'],
        ['unauthorized'],
        ['method_not_allowed'],
        ['unsupported_media_type'],
        ['internal_server_error'],
        ['resource_not_found', 'assignment'],
    ]
    
    response_dict = build_fields('getStudentsOfAnAssignment', response_types)
    
    parameters = [openapi.Parameter(
        'exh_id',
        in_=openapi.IN_QUERY,
        description='The id of the exhibition assignment',
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
        Get all students of an assignment. 
        '''
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
        try:
            response = {}
            data = {}
            req_data = request.GET
            serialized_request = serialize_request(request)
            log.debug("{} START".format(request_details(request)))
            exh_id = req_data.get('exh_id')

            try:
                log.debug("{} VALID DATA".format(request_details(request)))
                exhibition_actual = Exhibition.objects.filter(id=exh_id,instructor_fk_id=decoded['user_id']).values()
                if(len(exhibition_actual) == 0):
                    exhibition_actual = AssignedExhibitionInstructor.objects.filter(assignment_fk_id=exh_id,instructor_fk_id=decoded['user_id']).values()
                    if(len(exhibition_actual) == 0):
                        raise ApplicationError(['resource_not_found', 'assignment'])
                
                student_list = AssignedExhibitionStudents.objects.filter(assignment_fk_id=exh_id).values()
                
                status_code, message = get_code_and_response(['success'])
                
                content = {}
                content[MESSAGE] = message
                header_data = {}
                header_data["students"] = []
                for a in student_list:
                    st = Users.objects.filter(id=a['student_fk_id']).values()[0]
                    data = {}
                    data["id"] = a['student_fk_id']
                    data["name"] = st['name']
                    data["surname"] = st['surname']

                    header_data["students"].append(data)

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
                MESSAGE: "Failed to fetch students."
            }
            return Response(content, status=status_code)

        return Response(data[CONTENT], status=data[STATUS_CODE])
    

def filterExhibitions(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    input = str(request.GET.get('filter'))
    flag = False
    for type in ExhibitionStatus.STATUS_CHOICES:
        if(input.__eq__(type[0]) or input.__eq__(type[1])):
            flag = True
            break
    if( flag == False ):
        return HttpResponseNotAllowed('This is not an option') 
    
    template = loader.get_template('web_app/teacher/filter_exhibitions.html')
    context = {
		'title': "Filter Exhibitions",
		'header_content': 'Index header content',
        'userID': decoded['user_id'],
        'email': decoded['sub'],
        'name': decoded['name'],
        'surname': decoded['surname'],
        'organization': decoded['organization'],
        'role': decoded['role'],
        'value': input
	}   

    
    return HttpResponse(template.render(context, request)) 


def assessmentHandle(request):
    access_tkn = request.COOKIES.get('access_tkn')
    refresh_tkn = request.COOKIES.get('refresh_tkn')
    if not access_tkn:
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    tkn_okay, instr, decoded = at.authenticateInstructor(request,settings)
    if( tkn_okay == False):
        url = reverse('login')
        return HttpResponseRedirect(url)
    
    if( instr == False):
        return HttpResponseRedirect('/web_app/student/dashboard/')
    
    valid_s = AssignedExhibitionStudents.objects.filter(student_fk_id=request.GET.get('s'), assignment_fk=request.GET.get('q')).values()
    
    if(len(valid_s) == 0):
        url = reverse('display403')
        return HttpResponseRedirect(url)
    
    advisory = AssignedExhibitionInstructor.objects.filter(instructor_fk_id=decoded['user_id'], assignment_fk=request.GET.get('q')).values()
    if(len(advisory) != 0):
        template = loader.get_template('web_app/teacher/assessment/coadvisor.html')
        context = {
		    'title': "Student Assessment",
		    'header_content': 'Index header content',
            'userID': decoded['user_id'],
            'email': decoded['sub'],
            'name': decoded['name'],
            'surname': decoded['surname'],
            'organization': decoded['organization'],
            'role': decoded['role'],
            'student_id':request.GET.get('s'),
            'exh_id':request.GET.get('q')
	    }   

        return HttpResponse(template.render(context, request)) 
    else:  
        template = loader.get_template('web_app/teacher/assessment/main_advisor.html')
        stud = Users.objects.filter(id=request.GET.get('s')).values()[0]
        pre_ass = "Enter Assessment"

        try:
            uniqueCheck = GeneralAssessment.objects.filter(instructor_fk_id=decoded['user_id'],assignment_fk_id=request.GET.get('q'),student_fk_id=request.GET.get('s')).values()[0]
            pre_ass = uniqueCheck['assessement']
        except Exception as e:
            pass

        context = {
	    	'title': "Student Assessment",
	    	'header_content': 'Index header content',
            'userID': decoded['user_id'],
            'email': decoded['sub'],
            'name': decoded['name'],
            'surname': decoded['surname'],
            'organization': decoded['organization'],
            'role': decoded['role'],
            'student_id':request.GET.get('s'),
            'exh_id':request.GET.get('q'),
            'f_name': stud['name'],
            'l_name': stud['surname'],
            'assessment': pre_ass,
	    }   

        return HttpResponse(template.render(context, request)) 
    

