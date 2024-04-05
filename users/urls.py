from django.urls import path, include
from users import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path('api/login/', include('rest_social_auth.urls_knox')),
    path("", views.homepage, name="homepage"),
]
