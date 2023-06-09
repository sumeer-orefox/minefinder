from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.is_buyer = True
        user.is_active = True
        
        user.set_password(password)
        user.save()
        return user
    def create_seller(self, email, password, **extra_fields):
        user = self.create_user(email, password,**extra_fields)

        user.is_seller = True
        user.is_buyer = False
        
        user.save(using=self._db)

        return user
    def create_seller_buyer(self, email, password, **extra_fields):
        user = self.create_user(email, password,**extra_fields)

        user.is_seller = True
        user.is_buyer = True
        
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_seller', True)
        extra_fields.setdefault('is_buyer', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
    def get_by_natural_key(self, email, username="default"):
        return self.get(email=email, username=username)