from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer, GoogleSocialConnectSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from user.models import MyUser, GoogleProfile



class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        username = data['username']
        user = MyUser.objects.get(username=username)
        login(request, user)
        return Response(data, status=status.HTTP_200_OK)




class GoogleSocialConnect(LoginRequiredMixin, GenericAPIView):

    serializer_class = GoogleSocialConnectSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])

        goprofile, created   = GoogleProfile.objects.get_or_create(user = request.user)
        goprofile.google_id  = data['user_id']
        goprofile.email      = data['email']
        goprofile.full_name  = data['name']
        goprofile.first_name = data['first_name']
        goprofile.last_name  = data['last_name']
        goprofile.save()

        return Response(data, status=status.HTTP_200_OK)


