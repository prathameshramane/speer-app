from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import NotesViewSet, NotesFilterView, ShareNoteAPIView

notes_router= DefaultRouter()
notes_router.register('notes', NotesViewSet, basename='notes')
notes_router.register('search', NotesFilterView, basename='notes-search')

urlpatterns= [
    path('', include(notes_router.urls), name= 'notes-router'),
    path('notes/<int:pk>/share', ShareNoteAPIView.as_view(), name= 'share-note'),
]