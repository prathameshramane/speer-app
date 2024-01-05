from rest_framework.routers import DefaultRouter

from .views import NotesViewSet, NotesFilterView

notes_router= DefaultRouter()
notes_router.register('notes', NotesViewSet, basename='notes')
notes_router.register('search', NotesFilterView, basename='notes-search')

urlpatterns= notes_router.urls