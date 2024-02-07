from django import forms
from .models import Bug, Attachment


class BugForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)
    file = forms.FileField(required=False)
