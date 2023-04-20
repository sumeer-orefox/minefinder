from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from random import choices
from django.utils import timezone
from users.models import User
from django.contrib.postgres.fields import ArrayField
class Project(models.Model):
    
    PROJECT_STAGES = (
        ('UP', 'Unrecognised Potential'),
        ('HM', 'Historical Mine'),
        ('EM', 'Evidence of Mineralization'),
        ('OR', 'Ore Grades Present'),
        ('MR', 'Multiple Ore Grade Intersections'),
        ('RS', 'Resources'),
        ('EF', 'Extractable Feasibility'),
        ('OTHER', 'Other'),
    )
    RESOURCE_TYPE = (
        ('INDICATED' ,'Indicated'),
        ('INFERRED', 'Inferred'), 
        ('MEASURED' , 'Measured'),
        ('EXPLORATION', 'Exploration Target'),
        ('OTHER', 'Other'),
         ('NONE', 'None')
    )
    PERMIT_TYPE = (
        ('EPM', 'Exploration Permit'),
        ('MDL', 'Mineral Development Licence'),
        ('ML', 'Mining Lease'),
        ('IN', 'Infrastructure Permit'),
        ('MISC', 'Miscellaneous Licence')
    )
    PROJECT_TYPE = (
        ('GF', 'Greenfield Project'),
        ('BF', 'Brownfield Project'),
        ('OTHER', 'Other'),
        
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.PointField(srid=4326)  # SRID for WGS84
    location_desc = models.CharField(max_length=200,blank=True, null=True)
    project_stage = models.CharField(max_length=13, choices=PROJECT_STAGES,default='UP')
    estimated_resources = models.DecimalField(max_digits=10, decimal_places=2)
    resource_type = models.CharField(max_length=22, choices=RESOURCE_TYPE,default='INDICATED')
    exploration_upside = models.TextField(blank=True, null=True)
    regional_deposits = models.TextField(blank=True, null=True)
    ownership = models.TextField(blank=True, null=True)
    permit_type = models.CharField(max_length=24, choices=PERMIT_TYPE,default='EPM')
    permit_number = models.CharField(max_length=200,blank=True, null=True)
    main_commodity = models.CharField(max_length=200,blank=True, null=True)
    other_commodities = models.TextField(blank=True, null=True)
    project_type = models.CharField(max_length=13, choices=PROJECT_TYPE, default="BF")
    date_posted = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    public_fields = ArrayField(models.BooleanField(default=False), default=list, blank=True, null=True)

    def __str__(self):
        return self.title
    def label_from_instance(self, obj):
        """
        Convert objects into strings and generate the labels for the choices
        presented by this object. Subclasses can override this method to
        customize the display of the choices.
        """
        print("obj2",obj)
        return str(obj)
    class Meta:
        ordering = ("date_posted",)    
    
