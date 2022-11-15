
from django.contrib.auth import authenticate
from user.models import MyUser, GoogleProfile
from project.settings import SOCIAL_SECRET
import random




def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not MyUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)




def register_social_user(provider, user_id, email, name, first_name, last_name, avatar_url, email_verified):
    filtered_user_by_email = GoogleProfile.objects.filter(email=email)

    if filtered_user_by_email.exists():
        user = filtered_user_by_email[0].user
        return {
            'username': user.username,
            'email': user.email,
            'tokens': user.tokens()}

    else:
        user = {
            'username': generate_username(name), 
            'email': email,
            'password': SOCIAL_SECRET}
        user = MyUser.objects.create_user(**user)
        
        user.is_verified   = email_verified
        user.first_name    = first_name
        user.last_name     = last_name
        user.avatar_url    = avatar_url
        user.auth_provider = provider
        user.save()

        goprofile = GoogleProfile.objects.create(user=user)
        goprofile.google_id = user_id
        goprofile.email = email
        goprofile.full_name = name
        goprofile.first_name = first_name
        goprofile.last_name = last_name
        goprofile.save()

        new_user = authenticate(
            username=user.username, password=SOCIAL_SECRET)
        
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }

