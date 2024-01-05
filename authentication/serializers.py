from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from rest_framework.serializers import ModelSerializer, ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class SpeerUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

class UserSerializer(ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email']
        extra_kwargs= {
            'password': {
                'write_only': True
            }
        }

    def validate_password(self, data):
            validators.validate_password(password=data, user=User)
            return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user
    
    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        
        errors = dict() 
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        
        if errors:
            raise ValidationError(errors)
        
        return super(UserSerializer, self).validate(data)