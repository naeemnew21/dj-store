from django.shortcuts import render



def google_sign(request):
    return render(request, 'google.html')
