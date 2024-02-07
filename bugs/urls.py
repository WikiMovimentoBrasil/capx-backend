from django.urls import path
from . import views

app_name = "bugs"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("new/", views.bug_form, name="register_bug"),
    path("bug_list/", views.bug_list, name="bug_list"),
    path("<int:bug_id>/", views.bug_detail, name="bug_detail")
]