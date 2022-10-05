from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
import os
from project import settings
from django.core.files.storage import FileSystemStorage
from random import choice
from string import ascii_lowercase, digits
import datetime



def validate_name(name):
    if not(name) or name.isspace():
         raise ValidationError(_('empty name is not valid name'))   

         


def generate_name(length=4, chars = ascii_lowercase+digits):
    '''generate name from two sections
        1. random name of 4 letters from chars list
        2. current data and time
    '''
    random_name = ''.join([choice(chars) for i in range(length)])
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y%m%d%H%M%S")
    return "%s-%s"%(random_name, dt_str)



def image_upload(instance, filename):
    imgname, *exten = filename.split(".")
    new_name = generate_name() 
    return "user/%s.%s"%(new_name, exten[-1])



class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length = None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
    
    

AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}

    
    

class MyUser(AbstractUser):
    email         = models.EmailField(verbose_name="email address", unique=True, blank=False, null=False)
    phone_regex   = RegexValidator(regex="[0][1][0125][0-9][ ]?\d{3}[ ]?\d{4}", message="Phone number must be entered in the format: '01xx xxx xxxx'. Up to 11 digits allowed.")
    phone         = models.CharField(validators=[phone_regex], max_length=11, blank=False, null=False) # validators should be a list
    first_name    = models.CharField(verbose_name="first name", validators=[validate_name], max_length=30, blank=False, null=False)
    last_name     = models.CharField(verbose_name="last name", validators=[validate_name], max_length=30, blank=False, null=False)
    
    avatar        = models.ImageField(upload_to=image_upload, default = 'user/avatar.png', storage = OverwriteStorage() )
    avatar_url    = models.URLField(blank=True, null=True) # incase of provider = google
    address       = models.CharField(max_length=150, blank=True, null=True )
    
    is_verified   = models.BooleanField(default=False)
    auth_provider = models.CharField(
                                        max_length=255, blank=False, null=False,
                                        default=AUTH_PROVIDERS.get('email'))

    seller        = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.email


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    
    @property
    def get_name(self):
        name = self.first_name
        if self.last_name:
            name += ' ' + self.last_name
        return name
        
    