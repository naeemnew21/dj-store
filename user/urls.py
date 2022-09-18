from django.urls import path
from . import views 

app_name = 'user'


urlpatterns = [

    path('login', views.login_view , name = 'login'),
    path('logout', views.logout_view , name = 'logout'),
    path('sign-up', views.Registeration.as_view() , name = 'sign-up'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    

]

