from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from . import models
from . import serializers


class UserViewset(viewsets.ModelViewSet):
    serializer_class = serializers.FlatUserSerializer
    queryset = models.User.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.FlatUserSerializer
        return serializers.UserLoginSerializer
    
    def create(self, request):
        phone = request.data.get("phone", None)
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        
        if phone and password:
            user = models.PhoneOrEmailModelBackend.authenticate(self, username=phone, password=password)
            login(request, user, backend="account.models.PhoneOrEmailModelBackend")
        
        if email and password:
            user = models.PhoneOrEmailModelBackend.authenticate(self, username=email, password=password)
            login(request, user, backend="account.models.PhoneOrEmailModelBackend")

        return Response({
            "description": "User logged in successfully!"
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["get"])
    def logout_request(self, request):
        logout(request)
        
        return Response({
            "description": "logged out successfully!"
        }, status=status.HTTP_200_OK)