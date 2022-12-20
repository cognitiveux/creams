from .views import *

from django.http.response import FileResponse
from django.http import HttpResponseForbidden


def login_screen(request):
    access, payload = at.authenticate(request,settings)
    if access:
        if(payload.get('role') == INSTRUCTOR):
            url = reverse('teacher/dashboard')
            
        elif(payload.get('role') == STUDENT):
            url = reverse('student/dashboard')
            
        return HttpResponseRedirect(url)
    template = loader.get_template('web_app/account-management/sign-in.html')
    context = {
		'title': "Login",
		'header_content': 'Index header content'
	}
    
    return HttpResponse(template.render(context, request))


def signup_screen(request):
    template = loader.get_template('web_app/account-management/sign-up.html')
    context = {
		'title': "Sign Up",
		'header_content': 'Index header content',
        'organizations' : [oc[0] for oc in OrganizationModel.ORGANIZATION_CHOICES],
        'roles' : [r[0] for r in RoleModel.ROLE_CHOICES],
        'student_choices' : [r[0] for r in ClassAndLevelModel.STUDENT_CHOICES],
        'teacher_choices' : [r[0] for r in ClassAndLevelModel.TEACHER_CHOICES],

	}

    return HttpResponse(template.render(context, request))


def verifyAccount(request):
    template = loader.get_template('web_app/account-management/verifyemail.html')
    context = {
		'title': "Verify Account",
		'header_content': 'Index header content',
	}

    return HttpResponse(template.render(context, request))

# IMPORTANT: Always remember that urls are unique
def media_access(request, path):    
    used_path = 'images/' + path
    image = Exhibition.objects.filter(image=used_path, status="Published").values()    
    if(len(image) == 1 ):
        image = image[0]
        log.debug("{} accessed {} as a thumbnail of a publically available exhibition".format(request_details(request), used_path))
        used_path = 'media/images/' + path
        img = open(used_path, 'rb')
        response = FileResponse(img)
        return response
    
    image = Artwork.objects.filter(src=used_path).values()
    if(len(image) == 1 ):
        image = image[0]
        outart = OutdoorArtwork.objects.filter(artwork_fk_id=image['id']).values()
        if ( len(outart) > 0 ):
            log.debug("{} accessed {} as an open image".format(request_details(request), used_path))
            used_path = 'media/images/' + path
            img = open(used_path, 'rb')
            response = FileResponse(img)
            return response

    access_granted,decoded = at.authenticate(request,settings)
    #FIXME add code for other model checks
    if access_granted:
        image = Artwork.objects.filter(src=used_path,user_fk_id=decoded['user_id']).values()
        if ( len(image) > 0 ):
            log.debug("{} accessed {} as an artwork owner".format(request_details(request), used_path))
            used_path = 'media/images/' + path
            img = open(used_path, 'rb')
            response = FileResponse(img)
            return response

        image = Exhibition.objects.filter(image=used_path).values()
        if ( len(image) > 0 ):
            image2 = image[0]
            coadv = AssignedExhibitionInstructor.objects.filter(assignment_fk_id=image2["id"],instructor_fk_id=decoded['user_id']).values()
            main = image2['instructor_fk_id']
            stud = AssignedExhibitionStudents.objects.filter(assignment_fk_id=image2["id"],student_fk_id=decoded['user_id']).values()
            if ( len(coadv) > 0 ):
                log.debug("{} accessed exhibition {} thumbnail {} as a coadvisor".format(request_details(request),image2['id'], used_path))
                used_path = 'media/images/' + path
                img = open(used_path, 'rb')
                response = FileResponse(img)
                return response
            elif(main == decoded['user_id']):
                log.debug("{} accessed exhibition {} thumbnail {} as a main advisor".format(request_details(request),image2['id'], used_path))
                used_path = 'media/images/' + path
                img = open(used_path, 'rb')
                response = FileResponse(img)
                return response
            elif(len(stud) > 0):
                log.debug("{} accessed exhibition {} thumbnail {} as a student".format(request_details(request),image2['id'], used_path))
                used_path = 'media/images/' + path
                img = open(used_path, 'rb')
                response = FileResponse(img)
                return response
        
    #if access_granted == False:
    #    #redirect to login
    #    return HttpResponseForbidden('Not authorized to access this media. CHECK') 
    used_path = 'media/images/' + path
    img = open(used_path, 'rb')
    response = FileResponse(img)
    return response
    log.debug("{} request access to {}".format(request_details(request),used_path))
    return HttpResponseForbidden('Not authorized to access this media. CHECK')      


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


def display403(request):
    template = loader.get_template('web_app/errors/403.html')
    context = {
		'title': "Unauthorized Access",
		'header_content': 'Index header content',
	}   

    
    return HttpResponse(template.render(context, request)) 


def resetPass(request):
    access, payload = at.authenticate(request,settings)
    if access:
        if(payload.get('role') == INSTRUCTOR):
            url = reverse('teacher/dashboard')
            
        elif(payload.get('role') == STUDENT):
            url = reverse('student/dashboard')
            
        return HttpResponseRedirect(url)
    template = loader.get_template('web_app/account-management/reset-password.html')
    context = {
		'title': "Reset Password",
		'header_content': 'Index header content',
	}   

    
    return HttpResponse(template.render(context, request)) 
