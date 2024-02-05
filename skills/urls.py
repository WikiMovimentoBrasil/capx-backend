from django.urls import path, include
from skills import views

urlpatterns = [
    path('skill/new', views.SkillCreate.as_view(), name='skill_new'),
    path('skill/list', views.SkillList.as_view(), name='skill_list'),
    path('skill/<int:pk>/view', views.SkillView.as_view(), name='skill_view'),
    path('skill/<int:pk>/edit', views.SkillUpdate.as_view(), name='skill_edit'),
    path('skill/<int:pk>/delete', views.SkillDelete.as_view(), name='skill_delete'),
]