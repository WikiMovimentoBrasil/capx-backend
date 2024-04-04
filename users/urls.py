from django.urls import path, include
from users import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path('api/login/', include('rest_social_auth.urls_knox')),
    path("login/", views.login_oauth, name="login"),
    path("oauth/", include("social_django.urls", namespace="social_django")),
    path("logout/", views.logout, name="logout"),
    path("", views.homepage, name="homepage"),
]
