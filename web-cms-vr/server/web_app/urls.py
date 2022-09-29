from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from . import views_artworks
from . import views_account
from . import views_teacher
from . import views_blockchain

# Create the schema view for the API documentation
schema_view = get_schema_view(
	openapi.Info(
		title="CREAMS API",
		default_version='v1',
		description="The endpoints for interacting with the CREAMS server",
		terms_of_service="http://www.creams-project.eu/",
		contact=openapi.Contact(email="admin@cognitiveux.com"),
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	url(r'^demo(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	url(r'^demo/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	url(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
	url('index', views.index, name='index'),
	# Multimedia Handling
 	#path('media/images/<str:path>', views.media_access, name='media'),
  	#path('media/images/', views.media_access, name='media'),
    # Endpoints 
	url(r'^account-mgmt/activate-account$', views_account.AccountMgmtActivateAccount.as_view(), name='account-mgmt/activate-account'),
	url(r'^account-mgmt/create-user$', views_account.AccountMgmtCreateUser.as_view(), name='account-mgmt/create-user'),
	url(r'^account-mgmt/login$', views_account.AccountMgmtLogin.as_view(), name='account-mgmt/login'),
	url(r'^account-mgmt/logout$', views.logout, name='account-mgmt/logout'),
	url(r'^account-mgmt/poll-reset-email-status$', views_account.AccountMgmtPollResetEmailStatus.as_view(), name='account-mgmt/poll-reset-email-status'),
	url(r'^account-mgmt/poll-verification-email-status$', views_account.AccountMgmtPollVerificationEmailStatus.as_view(), name='account-mgmt/poll-verification-email-status'),
	url(r'^account-mgmt/refresh-token$', views_account.AccountMgmtRefreshToken.as_view(), name='account-mgmt/refresh-token'),
	url(r'^account-mgmt/request-account-verification-code$', views_account.AccountMgmtRequestAccountVerificationCode.as_view(), name='account-mgmt/request-account-verification-code'),
	url(r'^account-mgmt/request-password-reset-code$', views_account.AccountMgmtRequestPasswordResetCode.as_view(), name='account-mgmt/request-password-reset-code'),
	url(r'^account-mgmt/reset-password$', views_account.AccountMgmtResetPassword.as_view(), name='account-mgmt/reset-password'),
	url(r'^account-mgmt/update-password$', views_account.AccountMgmtUpdatePassword.as_view(), name='account-mgmt/update-password'),
	url(r'^artworks/details$', views.getArtwork.as_view(), name='getArtwork'),
	url(r'^artworks/student_list$', views.getStudentsArtworks.as_view(), name='getStudentsArtworks'),
	url(r'^artworks/outdoor_list$', views_artworks.getAllOutdoorArtworks.as_view(), name='getAllOutdoorArtworks'),
	url(r'^artworks/outdoor_list/sorted$', views.getAllOutdoorArtworksSorted.as_view(), name='getAllOutdoorExhibitions'),
	url(r'^artworks/create$', views.ArtworkCreate.as_view(), name='artworks/create'),
	url(r'^exhibitions/outdoor/details$', views.getOutdoorExhibition.as_view(), name='getOutdoorExhibition'),
	url(r'^exhibitions/outdoor/all$', views.getAllOutdoorExhibitions.as_view(), name='getAllOutdoorExhibitions'),
	url(r'^exhibitions/outdoor/all/sorted$', views.getAllOutdoorExhibitionsSorted.as_view(), name='getAllOutdoorExhibitionsSorted'),
	url(r'^exhibitions/outdoor/submit_artwork$', views.submitOutdoorArtwork.as_view(), name='submitOutdoorArtwork'),
 	url(r'^exhibitions/templates/fetch$', views.getVRTemplate.as_view(), name='getVRTemplate'),
	url(r'^sample_authenticated$', views.SampleAuthenticated.as_view(), name='sample_authenticated'),
 	url(r'^assignment/create$', views.ExhibitionCreate.as_view(), name='assignment/create'),
 	url(r'^assignment/assign_student$', views.AssignExhibition.as_view(), name='assignment/assign_student'),
	url(r'^teacher/other_users$', views.getAllUsers.as_view(), name="getAllUsers"),
	#url(r'^exhibitions/indoor/filter$', views.getFilteredExhibitions.as_view(), name="getFilteredExhibitions"),
    # Pages
    # Teacher
 	url(r'^teacher/dashboard/$', views_teacher.teacher_dashboard, name='teacher/dashboard'),
  	url(r'^teacher/assessment/$', views_teacher.teacher_assessment, name='teacher/assessment'),
  	url(r'^teacher/exhibition/$', views_teacher.teacher_exhibition, name='teacher/exhibition'),
  	url(r'^teacher/student_selection/$', views_teacher.student_selection_by_teacher, name='teacher/student_selection'),
  	url(r'^teacher/student_assessment/$', views_teacher.student_assessment_by_teacher, name='teacher/student_selection'),
  	url(r'^teacher/assessment/coadvisor/$', views_teacher.coadvisor_assessment, name='teacher/assessment/coadvisor'),
  	url(r'^teacher/assessment/main/$', views_teacher.main_assessment, name='teacher/assessment/main'),
    # Tools
    url('submit_artwork.html', views.submit_artwork, name='submit_artwork.html'),
   	url('artwork_submit', views.insertArtwork,name="test/submit"),
    url('add_artwork_to_outdoor', views.submit_outdoor_artwork_to_exhibition_page, name='submit_outdoor_artwork.html'),
   	url('outdoor_submit', views.outdoor_artwork_submit,name="outdoor/submit"),
    url('create_outdoor_exhibition', views.create_outdoor,name="outdoor/create"),
   	url('temporary_name', views.outdoor_exhibition_submit,name="test/outdoor_exhibition_submit"),
    # Util Pages
    url(r'^login/$', views.login_screen, name='login'),
    url(r'^sign-up/$', views.signup_screen, name='signup_screen'),
    url(r'^verify-account/$', views.verifyAccount, name='sverifyAccount'),
    # Student
    url(r'^student/dashboard/$', views.student_dashboard, name='student/dashboard'),
    url(r'^student/artworks/$', views.student_artworks, name='student/artworks'),
    url(r'^student/exhibitions/$', views.student_exhibitions, name='student/exhibitions'),
    # Virtual Reality
    url(r'^hardcoded_exhibition/$', views.vr_exhibition_demo, name='VR-DEMO'),
    url(r'^editor/picasso/$', views.editor_prototype, name='EDITOR-DEMO'),
    # Augemented Reality
    url(r'^create_ar/$', views.createAr, name='createAr'),
    # Visitor
    url(r'^visitor/dashboard/$', views.visitor_dashboard,name="visitor/dashboard"),
    url(r'^visitor/ar_display/$', views.ar_display,name="visitor/ar_display"),
    # Blockchain
    #url(r'^get_chain$', views_blockchain.get_chain, name="get_chain"),
    #url(r'^mine_block$', views_blockchain.mine_block, name="mine_block"),
    #url(r'^is_valid$', views_blockchain.is_valid, name="is_valid"),
    # Errors
	url(r'^403$', views.display403, name="display403"),

]