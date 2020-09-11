from rest_framework import serializers

from . import models
from .utils import *


class FlatUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = (
            "id",
            "name",
            "phone",
            "password",
            "email"
        )


class UserLoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = (
            "phone",
            "email",
            "password"
        )
        
    def validate(self, validated_data):
        phone = validated_data.get("phone")
        email = validated_data.get("email")
        password = validated_data.get("password")
        
        if email:
            is_email = check_email(email)
            if not is_email:
                raise serializers.ValidationError({"email": ["Email not in correct format!", ]})
        
        if phone:
            phone = check_bd_phone_number(phone)
            if not phone:
                raise serializers.ValidationError({"phone": ["Phone number not in correct format!", ]})
        
        if len(password) < 8:
            raise serializers.ValidationError({"password": ["Password must need more than 7 charecter!", ]})
        
        if phone:
            user = models.PhoneOrEmailModelBackend.authenticate(self, phone=phone, password=password)
        else:
            user = models.PhoneOrEmailModelBackend.authenticate(self, email=email, password=password)
        
        if not user:
            raise serializers.ValidationError({"username": ["Email / Phone number or Password not matched!", ]})
        
        return validated_data