from django.urls import path
from .views import skill_list, skill_detail

urlpatterns = [
    path('skills/', skill_list),
    path('skill/<int:id>/', skill_detail)
]
