from django.urls import path
from .views import (
    IndexView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TaskUndoDoneView,
    TagCreateView,
    TagsListView,
    TagUpdateView,
    TagDeleteView
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create-task/", TaskCreateView.as_view(), name="create-task"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("create-tag/", TagCreateView.as_view(), name="create-tag"),
    path("tags/", TagsListView.as_view(), name="tags"),
    path(
        "tags/<int:pk>/update/",
        TagUpdateView.as_view(),
        name="tag-update"
    ),
    path(
        "tags/<int:pk>/delete/",
        TagDeleteView.as_view(),
        name="tag-delete"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path("tasks/<int:pk>/undo-done/", TaskUndoDoneView.as_view(), name="task-undo-done"),
]

app_name = "todo_app"
