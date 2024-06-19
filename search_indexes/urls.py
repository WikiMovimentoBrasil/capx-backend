from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .viewsets import UsersDocumentViewSet

router = DefaultRouter()
users = router.register(r'users', UsersDocumentViewSet, basename='usersdocument')

urlpatterns = [
    path('', include(router.urls)),
]