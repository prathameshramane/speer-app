from rest_framework.routers import DefaultRouter

from .views import NotesViewSet

notes_router= DefaultRouter()
notes_router.register('', NotesViewSet, basename='notes')

urlpatterns= notes_router.urls