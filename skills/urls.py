from django.urls import path, include
from .views import SkillViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('skill', SkillViewSet, basename='skill')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),
]
