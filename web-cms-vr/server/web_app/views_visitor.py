from .views import *
from django.http import HttpResponseForbidden

def visitor_dashboard(request):

    template = loader.get_template('web_app/visitor/landingpage.html')
    context = {
		'title': "Visitor Dashboard",
		'header_content': 'Index header content',
	}   
        
    return HttpResponse(template.render(context, request))

def ar_display(request):
    assigned_id = request.GET.get('assign')
    #if exh['status'] != 'Published':
    #    return HttpResponseForbidden('Not authorized to access this media. CHECK')

    outdoor = OutdoorExhibition.objects.filter(id = assigned_id).values()[0]
    print(outdoor)
    exh = Exhibition.objects.filter(id=outdoor['exhibition_fk_id']).values()
    titleExh = exh[0]['exhibition_title']
    
    inst = Users.objects.filter(id=outdoor['user_fk_id']).values()[0]
    full_name = inst["name"] + " " + inst["surname"]
    template = loader.get_template('web_app/visitor/ar_display.html')
    context = {
		'title': "View AR Exhibition",
		'header_content': 'Index header content',
        'exh_title': titleExh,
        'teacher': full_name,
        'exh_id': outdoor['id']
	}   

    return HttpResponse(template.render(context, request))

def vr_display(request):
    assigned_id = request.GET.get('assign')
    #if exh['status'] != 'Published':
    #    return HttpResponseForbidden('Not authorized to access this media. CHECK')

    virtual = VR_Exhibition.objects.filter(id = assigned_id).values()[0]
    print(virtual)
    exh = Exhibition.objects.filter(id=virtual['exhibition_fk_id']).values()
    titleExh = exh[0]['exhibition_title']
    
    temp = virtual['vr_exhibition']
    filename = "media/" + temp[0:len(temp)]
    payload = open(filename, "r").read()
    try:
        name = "media/" + virtual['vr_script']
        ac = open(name, "r").read()
    except Exception:
        ac = ' '
    template = loader.get_template('web_app/bases/vr_base.html')
    context = {
        'title': titleExh,
        'exh_id': virtual['id'],
        'custom_exhibition': payload,
        'x_script':ac
	}   

    return HttpResponse(template.render(context, request))

def vr_exhibition_demo(request):
    #template = loader.get_template('web_app/vr-exhibitions/picasso/picasso.html')
    template = loader.get_template('web_app/vr-exhibitions/picasso/template2.html')
    context = {
		'title': "Add artwork to an outdoor exhibition",
		'header_content': 'Index header content'
	}
    
    return HttpResponse(template.render(context, request))
