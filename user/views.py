from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from .utils import get_username
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, UserForm
from .models import MyUser

from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages







def pend_staff(user):
    return user.is_authenticated and user.seller
     


@user_passes_test(pend_staff, login_url='/login' )
def pending(request):
    if request.user.is_staff:
        return redirect('product:dashboard')
    return render(request, 'pending.html')


class Registeration(CreateView):
    form_class = SignUpForm
    template_name = 'register.html'
    success_url = reverse_lazy('product:index')
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.seller:
                return redirect('user:pending') 
            return redirect("product:index")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # first save form
        valid = super().form_valid(form)
    
        # then login
        email    = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        username = MyUser.objects.get(email = email).username
        user = authenticate(username = username, password = password)
        login(self.request, user)
        
        if user.seller:
            return redirect('user:pending')
        
        return valid
        #return HttpResponseRedirect(self.get_success_url())
    
    

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = UserForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('user:profile')
    login_url = reverse_lazy('user:login')
    
    def get_object(self, queryset=None):
        return self.request.user   
    

    
    
@requires_csrf_token
@csrf_exempt
@csrf_protect
def login_view(request):
    context = {'error':''}

    if request.user.is_authenticated:
        if request.user.seller:
            return redirect('user:pending') 
        return redirect("product:index")
    
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        username = get_username(username)
        
        user = authenticate(username=username, password=password)
        if user :
            login(request, user)
            if user.seller:
                return redirect('user:pending')
            return redirect("product:index")
        else :
            context['error'] = "Invalid Login" 
    return render(request, 'login.html' , context)


    
    
def logout_view(request):
    logout(request)
    return redirect('product:index')





def handle_404(request, exception):
    return render(request, 'error/404.html' , status=404 )


def handle_500(request, exception=None):
    return render(request,'error/500.html', status=500 )


def handle_403(request, exception=None):
    return render(request,'error/403.html', status=403 )



def handle_400(request, exception=None):
    return render(request,'error/403.html', status=403 )





def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = MyUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "reset/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'online-store.com',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return redirect ("/password_reset/done/")
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request, "reset/password_reset.html", {"password_reset_form":password_reset_form})




from project.settings import THEME_STYLE

def theme_context(request):
    theme = request.COOKIES.get(THEME_STYLE, None)
    
    if theme:
        return {THEME_STYLE: theme}
    else:
        return {THEME_STYLE: 'light'}




