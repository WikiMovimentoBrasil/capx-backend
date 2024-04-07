from django.urls import path, include
from .views import ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('api/login/', include('rest_social_auth.urls_knox')),
]
