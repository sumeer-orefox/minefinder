from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from random import choices
from django.utils import timezone
from django.contrib.auth.models import User
class Project(models.Model):
    PROJECT_STAGES = (
        ('UP', 'Unrecognised Potential'),
        ('HM', 'Historical Mine'),
        ('EM', 'Evidence of Mineralization'),
         ('OR', 'Ore Grades Present'),
        ('MR', 'Multiple Ore Grade Intersections'),
        ('RS', 'Resources'),
        ('EF', 'Extractable Feasibility'),
    )
    RESOURCE_TYPE = (
        ('INDICATED' ,'Indicated'),
        ('INFERRED', 'Inferred'), 
        ('MEASURED' , 'Measured'),
        ('EXPLORATION', 'Exploration Target'),
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
    slug = models.SlugField(unique=True)
    description = models.TextField()
    location = models.PointField(srid=4326)  # SRID for WGS84
    project_stage = models.CharField(max_length=3, choices=PROJECT_STAGES)
    estimated_resources = models.DecimalField(max_digits=10, decimal_places=2)
    resource_type = models.CharField(max_length=12, choices=RESOURCE_TYPE)
    exploration_upside = models.TextField(blank=True, null=True)
    regional_deposits = models.TextField(blank=True, null=True)
    ownership = models.TextField(blank=True, null=True)
    permit_type = models.CharField(max_length=4, choices=PERMIT_TYPE)
    permit_number = models.CharField(max_length=200)
    main_commodity = models.CharField(max_length=200)
    other_commodities = models.TextField(blank=True, null=True)
    project_type = models.CharField(max_length=13, choices=PROJECT_TYPE)
    date_posted = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
