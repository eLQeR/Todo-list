from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Worker, Tag, Task

admin.site.register(Worker, UserAdmin)
admin.site.register(Task)
admin.site.register(Tag)
