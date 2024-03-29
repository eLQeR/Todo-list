from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import  generic

from .forms import UserRegisterForm, TaskForm, TagForm
from .models import Task, Tag, Worker


class IndexView(generic.ListView):
    model = Task
    template_name = "index.html"
    queryset = Task.objects.all()
    context_object_name = "tasks"


class TagsListView(generic.ListView):
    model = Task
    template_name = "todo/tags.html"
    queryset = Tag.objects.all()
    context_object_name = "tags"

class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    template_name = "todo/tag-create.html"
    success_url = reverse_lazy("todo_app:tags")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "todo/tag-update.html"
    success_url = reverse_lazy("todo_app:tags")

class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    template_name = "todo/tag-delete-confirm.html"
    success_url = reverse_lazy("todo_app:tags")

class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task-create.html"
    success_url = reverse_lazy("todo_app:index")


    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            task = form.save()
            task.creator = request.user
            task.save()
            return HttpResponseRedirect(reverse_lazy("todo_app:index"))
        return HttpResponseBadRequest()



class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task-update.html"
    success_url = reverse_lazy("todo_app:index")

    def get(self, request, *args, **kwargs):
        if request.user != get_object_or_404(Task, pk=kwargs.get("pk")).creator:
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user != get_object_or_404(Task, pk=kwargs.get("pk")).creator:
            return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Task.objects.all()
    template_name = "todo/task-detail.html"
    context_object_name = "task"


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "todo/task-delete-confirm.html"
    success_url = reverse_lazy("todo_app:index")


class TaskUndoDoneView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task-confirm-undo.html"
    context_object_name = "task"

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.creator and request.user not in task.assignees.all():
            return HttpResponseForbidden()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.creator and request.user not in task.assignees.all():
            return HttpResponseForbidden()
        task.is_completed = not task.is_completed
        task.save()
        return HttpResponseRedirect(reverse_lazy("todo_app:index"))

class UserCreateView(generic.CreateView):
    model = Worker
    form_class = UserRegisterForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy("todo_app:index")
