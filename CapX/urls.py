"""
URL configuration for CapX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from .search import search
from rest_framework.routers import DefaultRouter
from skills.views import SkillViewSet
from users.views import ProfileViewSet, UsersViewSet


router = DefaultRouter()
router.register('skill', SkillViewSet, basename='skill')
router.register('users', UsersViewSet, basename='users')
router.register('profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search, name='search'),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('', include('social_django.urls')),
    path('bugs/', include('bugs.urls')),
    path('', include(router.urls)),
    path('<int:pk>/', include(router.urls)),
    path('api/login/', include('rest_social_auth.urls_knox')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)