from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from skills.models import Skill


class SkillList(ListView):
    model = Skill


class SkillView(DetailView):
    model = Skill


class SkillCreate(CreateView):
    model = Skill
    fields = ['skill_name', 'skill_description', 'skill_type', 'skill_wikidata_item']
    success_url = reverse_lazy('skill_list')


class SkillUpdate(UpdateView):
    model = Skill
    fields = ['skill_name', 'skill_description', 'skill_type', 'skill_wikidata_item']
    success_url = reverse_lazy('skill_list')


class SkillDelete(DeleteView):
    model = Skill
    success_url = reverse_lazy('skill_list')
