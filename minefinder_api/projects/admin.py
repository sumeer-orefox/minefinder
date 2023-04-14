from django.contrib import admin
from projects.models import Project
from .forms import ProjectForm

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
admin.site.register(Project,ProjectAdmin)
