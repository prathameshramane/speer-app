from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import FilterSet, CharFilter, DjangoFilterBackend

from .serializers import NotesSerializer, NotesDetailSerializer
from .models import Note

class NotesFilter(FilterSet):
    description= CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model= Note
        fields= ['description']

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
    

class NotesFilterView(ReadOnlyModelViewSet):
    permission_classes= (IsAuthenticated,)
    serializer_class= NotesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["description"]
    filterset_class= NotesFilter
    
    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
