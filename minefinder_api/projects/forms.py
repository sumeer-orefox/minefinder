from django import forms
from .models import Project
from django.contrib.gis.geos import Point


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'location','project_stage','estimated_resources','resource_type','exploration_upside',
                 'regional_deposits','ownership','permit_type','permit_number','date_posted', 'latitude', 'longitude' ] 

    latitude = forms.FloatField()
    longitude = forms.FloatField()
   
    
    def clean(self):
       
        data = super().clean()
        latitude = data.pop('latitude')
        longitude = data.pop('longitude')
        data['location'] = Point(latitude,longitude,srid=4326)
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location = self.initial.get('location')
        if(isinstance(location,Point)):
            self.initial['latitude'] = location.tuple[0]
            self.initial['longitude'] = location.tuple[1]
