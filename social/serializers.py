from rest_framework import serializers
from . import google
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from project.settings import GOOGLE_CLIENT_ID



class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        
        user_data = google.Google.validate(auth_token)
    
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id        = user_data['sub']
        email          = user_data['email']
        full_name      = user_data['name']
        first_name     = user_data['given_name']
        last_name      = user_data['family_name']
        avatar_url     = user_data['picture']
        email_verified = user_data['email_verified']
        provider       = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=full_name,
            first_name=first_name, last_name=last_name, avatar_url=avatar_url, email_verified=email_verified)


