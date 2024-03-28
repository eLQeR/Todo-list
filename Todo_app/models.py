from django.contrib.auth.models import AbstractUser
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Worker(AbstractUser):
    pass


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    creator = models.ForeignKey(
        to=Worker,
        on_delete=models.DO_NOTHING,
        related_name="own_tasks",
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="tasks", blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def get_date_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_deadline(self):
        if self.deadline:
            return self.deadline.strftime("%Y-%m-%d %H:%M:%S")
        return None

