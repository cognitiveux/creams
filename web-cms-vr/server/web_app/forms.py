from django.forms import ModelForm
from .models import *
from django import forms
    
class ExhibitionForm(ModelForm):
    message = forms.CharField(max_length=2000,required=False)
    ts_last_updated = forms.DateTimeField(required=False)
    instructor = forms.IntegerField(required=False)
    
    class Meta:
        model = Exhibition
        fields = '__all__'
        
              
class ArtWorkForm(ModelForm):  
    class Meta:  
        model = Artwork  
        fields = '__all__'  
        
class OutdoorArtWorkForm(ModelForm):  
    description = forms.CharField(max_length=500,required=False)
    ts_last_updated = forms.DateTimeField (required=False)

    class Meta:  
        model = OutdoorArtwork  
        fields = '__all__'          

class OutdoorExhibitionForm(ModelForm):
    class Meta:
        model= OutdoorExhibition
        fields = '__all__'        