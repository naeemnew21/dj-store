
from django.contrib.auth import authenticate
from user.models import MyUser
from project.settings import SOCIAL_SECRET
import random
from rest_framework.exceptions import AuthenticationFailed



def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not MyUser.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)




def register_social_user(provider, user_id, email, name, first_name, last_name, avatar_url, email_verified):
    filtered_user_by_email = MyUser.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
            user = MyUser.objects.get(email=email)
            registered_user = authenticate(
                username=user.username, password=SOCIAL_SECRET)

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

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

        new_user = authenticate(
            username=user.username, password=SOCIAL_SECRET)
        
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }
