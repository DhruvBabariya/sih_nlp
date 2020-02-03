from django import forms
from django.contrib.auth.models import User
from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'key', 'document','aspects']
