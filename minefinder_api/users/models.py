from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
import django.core.validators as validators
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from message_control.models import GenericFileUpload




class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=10, default="default", null=True, blank=True)
    #first_name = models.CharField(max_length=32,default="Admin")
    #last_name = models.CharField(max_length=32)
    #company = models.CharField(max_length=50,null=True, blank=True)
    #job_title = models.CharField(max_length=100,null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    #bio = models.TextField(null=True, blank=True)    
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_online = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    @property
    #def full_name(self):
    #    return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
    
    def natural_key(self):
        return (self.email, self.username)
    
    class Meta:
        ordering = ("date_joined",) 
    
class Jwt(models.Model):
    user = models.OneToOneField(
        User, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name="user_profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,default="user")
    last_name = models.CharField(max_length=100,default="test")
    caption = models.CharField(max_length=250,null=True, blank=True)
    company = models.CharField(max_length=50,null=True, blank=True)
    job_title = models.CharField(max_length=100,null=True, blank=True)
    contact_no = models.CharField(max_length=40,null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ForeignKey(
        GenericFileUpload, related_name="user_image", on_delete=models.SET_NULL, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("date_joined",)    
    def label_from_instance(self):
         return self.email

class Favorite(models.Model):
    user = models.OneToOneField(User, related_name="user_favorites", on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, related_name="user_favoured")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        ordering = ("created_at",)        