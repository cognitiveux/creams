from .views import *

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
    
    valid_q = Exhibition.objects.filter(id=request.GET['q'], instructor_fk_id=decoded['user_id']).values()
    
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
        'exh_id': request.GET['q']
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
