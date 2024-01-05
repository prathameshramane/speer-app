from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Note
from authentication.serializers import UserSerializer

class NotesSerializer(ModelSerializer):
    owner_username= SerializerMethodField()

    class Meta(object):
        model= Note
        fields= ['id', 'description', 'owner', 'owner_username']
        extra_kwargs= {
            'id': {
                'read_only': True
            },
            'owner': {
                'write_only': True
            },
            'owner_username': {
                'read_only': True
            }
        }

    def get_owner_username(self, obj:Note):
        return obj.owner.username


class NotesDetailSerializer(ModelSerializer):
    owner= SerializerMethodField()

    class Meta(object):
        model= Note
        fields= ['id', 'description', 'owner']

    def get_owner(self, obj: Note):
        return UserSerializer(obj.owner).data