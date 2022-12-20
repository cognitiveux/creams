from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.timezone import now


class OrganizationModel(models.Model):
	AUTH = "AUTH"
	CUT = "CUT"
	CUX = "CUX"
	NTNU = "NTNU"
	SHENKAR = "SHENKAR"
	UPAT = "UPAT"

	ORGANIZATION_CHOICES = (
		(AUTH, "AUTH"),
		(CUT, "CUT"),
		(CUX, "CUX"),
		(NTNU, "NTNU"),
		(SHENKAR, "SHENKAR"),
		(UPAT, "UPAT"),
	)


class RoleModel(models.Model):
	INSTRUCTOR = "INSTRUCTOR"
	STUDENT = "STUDENT"

	ROLE_CHOICES = (
		(INSTRUCTOR, "INSTRUCTOR"),
		(STUDENT, "STUDENT"),
	)
 
 
class ClassAndLevelModel(models.Model):
	A1 = "a1"
	A2 = "a2"
	B1 = "b1"
	B2 = "b2"
	C1 = "c1"
	C2 = "c2"
	D1 = "d1"
	D2 = "d2"
	PROFESSOR = "PROFESSOR"
	ASSOCIATE_PROFESSOR = "ASSOCIATE PROFESSOR"

	LEVEL_CHOICES = (
		(A1, "a1"),
		(A2, "a2"),
		(B1, "b1"),
		(B2, "b2"),
		(C1, "c1"),
		(C2, "c2"),
		(D1, "d1"),
		(D2, "d2"),
		(PROFESSOR, "PROFESSOR"),
		(ASSOCIATE_PROFESSOR, "ASSOCIATE PROFESSOR"),
	)

	STUDENT_CHOICES = (
		(A1, "a1"),
		(A2, "a2"),
		(B1, "b1"),
		(B2, "b2"),
		(C1, "c1"),
		(C2, "c2"),
		(D1, "d1"),
		(D2, "d2"),
	)

	TEACHER_CHOICES = (
		(PROFESSOR, "PROFESSOR"),
		(ASSOCIATE_PROFESSOR, "ASSOCIATE PROFESSOR"),
	)


class ExhibitionSpaceModel(models.Model):
	SeparateSpaces = "Separate Spaces"
	SharedRooms = "Shared Rooms"
	SharedFloor = "Shared Floor"
 
	SPACE_CHOICES = (
		(SeparateSpaces, "Separate Spaces"),
		(SharedRooms , "Shared Rooms"),
		(SharedFloor , "Shared Floor"),
	)
 
 
class ExhibitionStatus(models.Model):
	TemporaryStored = "Temporary Stored"
	AcceptingArtworks = "Accepting Artworks"
	ReadyToBeAssessed = "Ready to be Assessed"
	AssessmentStarted = "Assessment Started"
	Assessed = "Assessed"
	Published = "Published"
 
	STATUS_CHOICES = (
		(TemporaryStored , "Temporary Stored"),
		(AcceptingArtworks , "Accepting Artworks"),
		(ReadyToBeAssessed , "Ready to be Assessed"),
		(AssessmentStarted , "Assessment Started"),
		(Assessed , "Assessed"),
		(Published, "Published"),
	)
	
  
class Users(AbstractBaseUser):
	email = models.EmailField(max_length=50, unique=True)
	name = models.CharField(max_length=50)
	organization = models.CharField(max_length=15, choices=OrganizationModel.ORGANIZATION_CHOICES)
	password = models.CharField(max_length=500)
	role = models.CharField(max_length=15, choices=RoleModel.ROLE_CHOICES)
	surname = models.CharField(max_length=50)
	c_register_task_id = models.CharField(max_length=100, default="")
	c_reset_task_id = models.CharField(max_length=100, default="")
	ts_entry_added = models.DateTimeField(default=now)
	ts_last_updated = models.DateTimeField(default=now)
	class_level =	models.CharField(max_length=30,choices=ClassAndLevelModel.LEVEL_CHOICES)

	USERNAME_FIELD = 'email'


class ActiveUsers(models.Model):
	"""
	Contains information about users who have verified their accounts
	"""
	user_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE,
	)
	verification_code = models.CharField(max_length=50)
	ts_activation = models.DateTimeField(null=True, default=None)
	frequent_request_count = models.IntegerField(default=0) # number of requests made within an hour
	ts_added = models.DateTimeField(default=now)


class ResetPassword(models.Model):
	"""
	Contains reset password records
	"""
	def calculate_expiration():
		"""
		A function to fill the expiration time of the reset code
		Returns (datetime):
			The expiration time which is found in settings
		"""
		return now()+timedelta(seconds=settings.RESET_PASSWORD_INTERVAL)

	user_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE
	)
	frequent_request_count = models.IntegerField(default=0) # number of requests made within an hour
	reset_code = models.CharField(max_length=50)
	ts_expiration_reset = models.DateTimeField(null=True, default=calculate_expiration) # when this code will expire
	ts_reset = models.DateTimeField(null=True) # when the user actualy reset their password
	ts_requested = models.DateTimeField(default=now) # when this reset code was requested


class Exhibition(models.Model):
    exhibition_title = models.CharField(max_length=200)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    instructor_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE,
  		to_field='id',
		default=1,
	)
    space_assign = models.CharField(max_length=15, choices=ExhibitionSpaceModel.SPACE_CHOICES)
    message = models.CharField(max_length=2000, default=' ')
    image = models.ImageField(upload_to='images')
    status = models.CharField(max_length=30,choices=ExhibitionStatus.STATUS_CHOICES)
    ts_last_updated = models.DateTimeField(default=now)

    
    def __str__(self):
        return self.exhibition_title 
    
    
class AssignedExhibitionStudents(models.Model):
    class Meta:
        unique_together = (('student_fk', 'assignment_fk'),)

    student_fk = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='id')
    assignment_fk = models.ForeignKey(Exhibition, on_delete=models.CASCADE, to_field='id')

    
class AssignedExhibitionInstructor(models.Model):
    class Meta:
        unique_together = (('instructor_fk', 'assignment_fk'),)

    instructor_fk = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='id')
    assignment_fk = models.ForeignKey(Exhibition, on_delete=models.CASCADE, to_field='id')


class GeneralAssessment(models.Model):
    instructor_fk = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='id',related_name='instructor')
    assignment_fk = models.ForeignKey(Exhibition, on_delete=models.CASCADE, to_field='id')
    student_fk = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='id',related_name='student')
    assessement = models.CharField(max_length=2000)
    
    
class Artwork(models.Model):
    src = models.FileField(upload_to='images')
    name = models.CharField(max_length=200)
    user_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE,
		default=1,
  		to_field='id'
	)
    year =  models.IntegerField()
    height = models.DecimalField(max_digits=20, decimal_places=6)
    width = models.DecimalField(max_digits=20,  decimal_places=6)
    depth = models.DecimalField(max_digits=20,  decimal_places=6)
    unit = models.DecimalField(max_digits=20,   decimal_places=6)
    technique = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    art_type = models.CharField(max_length=200)
    
    def __str__(self):
        return self.src # + ' ' + self.start_date  + ' ' + self.end_date + ' ' + self.space_assign 
    
   
class OutdoorExhibition(models.Model):
    user_fk = models.ForeignKey(
		Users,
		on_delete=models.CASCADE,
  		default=1,
  		to_field='id'
	)
    exhibition_fk = models.ForeignKey(
		Exhibition,
		on_delete=models.CASCADE,
		to_field='id',
  		default=42,
	)
    
    def __str__(self):
        return self.title


class OutdoorArtwork(models.Model):
    artwork_fk =  models.ForeignKey(Artwork, on_delete=models.CASCADE, to_field='id')
    exhibition_fk =  models.ForeignKey(OutdoorExhibition, on_delete=models.CASCADE, to_field='id')
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lon = models.DecimalField(max_digits=20, decimal_places=15) 
    description = models.CharField(max_length=500, null=True)
    ts_last_updated = models.DateTimeField(default=now)

    
    def __str__(self):
        return self.lat + ' ' + self.lon
     
     
class VR_Templates(models.Model):
    basis = models.FileField(upload_to='templates')
    name = models.CharField(max_length=200)
    rooms = models.IntegerField()
    thumbnail = models.ImageField(upload_to='templates/thumbnails',null=True)
    
    def __str__(self):
        return self.basis
    


class VR_Exhibition(models.Model):
    #class Meta:
    #    unique_together = (('exhibition_fk', 'student_fk'),)
    student_fk = models.ForeignKey(
		Users,
  		on_delete=models.CASCADE, 
    	to_field='id'
	)
    exhibition_fk = models.ForeignKey(
		Exhibition,  		
  		on_delete=models.CASCADE, 
    	to_field='id'
	)
    vr_exhibition = models.FileField(upload_to='vr_exhibitions')
    vr_script = models.FileField(upload_to='vr_exhibitions/scripts',null=True)
    