from django.urls import path
from .views import SkillAPIView, SkillDetails

urlpatterns = [
    path('skill/', SkillAPIView.as_view()),
    path('skill/<int:id>/', SkillDetails.as_view())
]
