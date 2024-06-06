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
from skills.views import SkillViewSet, ListSkillViewSet
from users.views import ProfileViewSet, UsersViewSet, ListTerritoryViewSet, ListLanguageViewSet, ListWikimediaProjectViewSet
from bugs.views import BugViewSet, AttachmentViewSet
from orgs.views import OrganizationViewSet, ListOrganizationViewSet
from events.views import EventViewSet, EventParticipantViewSet, EventOrganizationsViewSet


router = DefaultRouter()
router.register('skill', SkillViewSet, basename='skill')
router.register('users', UsersViewSet, basename='users')
router.register('profile', ProfileViewSet, basename='profile')
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('bugs', BugViewSet, basename='bugs')
router.register('attachment', AttachmentViewSet, basename='attachment')
router.register('events', EventViewSet)
router.register('events_participants', EventParticipantViewSet)
router.register('events_organizations', EventOrganizationsViewSet)

# Alternative version of views, read-only and only returns the __str__ with the id as the key
router.register('list_language', ListLanguageViewSet, basename='list_language')
router.register('list_organizations', ListOrganizationViewSet, basename='list_organizations')
router.register('list_skills', ListSkillViewSet, basename='list_skills')
router.register('list_territory', ListTerritoryViewSet, basename='list_territory')
router.register('list_wikimedia_project', ListWikimediaProjectViewSet, basename='list_wikimedia_project')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search, name='search'),
    path('api-auth/', include("rest_framework.urls", namespace="rest_framework")),
    path('', include('social_django.urls')),
    path('', include(router.urls)),
    path('<int:pk>/', include(router.urls)),
    path('api/login/', include('rest_social_auth.urls_knox')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)