from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, UserProfile




class SignUpForm(UserCreationForm):
    agree = forms.BooleanField(error_messages={"required":"you must agree terms and conditions"})
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'seller','agree')



class UserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar')



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'birth_date', 'country', 'langs', 'company', 'company_url')



class SocialLinksForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('twitter_url', 'facebook_url', 'linkedin_url', 'instagram_url', 'quora_url', 'youtube_url')


