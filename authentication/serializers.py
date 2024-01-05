from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

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