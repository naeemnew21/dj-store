from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt, csrf_protect, requires_csrf_token
from .utils import get_username
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import SignUpForm
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






class Registeration(CreateView):
    form_class = SignUpForm
    template_name = 'sign-up.html'
    success_url = reverse_lazy('store:home')
    
    def form_valid(self, form):
        # first save form
        super().form_valid(form)
    
        # then login
        email    = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        username = MyUser.objects.get(email = email).username
        user = authenticate(username = username, password = password)
        login(self.request, user)
        
        return HttpResponseRedirect(self.get_success_url())
    
    
    
    
    
@requires_csrf_token
@csrf_exempt
@csrf_protect
def login_view(request):
    context = {'error':''}
    
    if request.user.is_authenticated: 
        return redirect("store:home")
    
    
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        username = get_username(username)
        
        user = authenticate(username=username, password=password)
        if user :
            login(request, user)
            return redirect("store:home")
        else :
            context['error'] = "Invalid Login" 
    return render(request, 'login.html' , context)


    
    
def logout_view(request):
    logout(request)
    return redirect('store:home')





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

