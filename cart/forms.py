from django import forms
from .models import CheckOut



class CheckOutCreateForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ('phone', 'country', 'city', 'add1', 'add2')



