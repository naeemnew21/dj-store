from django.urls import path
from . import views 

app_name = 'user'


urlpatterns = [
    path('login', views.login_view , name = 'login'),
    path('pending', views.pending , name = 'pending'),
    path('logout', views.logout_view , name = 'logout'),
    path('sign-up', views.Registeration.as_view() , name = 'sign-up'),
    path('profile', views.EditProfileView.as_view() , name = 'profile'),
    path('profileinfo', views.EditUserProfileView.as_view() , name = 'profileinfo'),
    path('profilelinks', views.EditSocialLinksView.as_view() , name = 'profilelinks'),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('move-to-cart', views.move_to_cart , name = 'move_to_cart'),
]
