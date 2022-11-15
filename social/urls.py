from django.urls import path
from . import api
from . import views

app_name = 'social'


urlpatterns = [
    
    path('google/', api.GoogleSocialAuthView.as_view()),
    path('google_connect/', api.GoogleSocialConnect.as_view()),
    path('login', views.google_sign, name = 'log'),

]

