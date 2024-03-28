from django import forms
from django.contrib.auth.forms import UserCreationForm

from Todo_app.models import Tag, Task, Worker


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "tags")


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = [
            "username", "email", "first_name",
            "last_name", "password1", "password2"
        ]