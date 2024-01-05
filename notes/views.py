from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import NotesSerializer, NotesDetailSerializer
from .models import Note

# Create your views here.
class NotesViewSet(ModelViewSet):
    permission_classes= (IsAuthenticated,)
    serializer_class= NotesSerializer
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def create(self, request):
        request.data['owner'] = request.user.pk
        return super(NotesViewSet, self).create(request=request)
    
    def update(self, request, *args, **kwargs):
        request.data['owner'] = request.user.pk
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = NotesDetailSerializer
        return super().retrieve(request, *args, **kwargs)

