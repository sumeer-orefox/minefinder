from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description', 'project_type','location','location_desc', 'project_stage','estimated_resources','resource_type','exploration_upside',
                 'regional_deposits','ownership','permit_type','permit_number','date_posted', 'main_commodity','other_commodities') 
