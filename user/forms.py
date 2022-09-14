from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser




class SignUpForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'seller')


    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     seller = self.cleaned_data['seller']
    #     self.cleaned_data['active'] = bool(seller)
    #     cleaned_data['active'] = bool(seller)
    #     return cleaned_data