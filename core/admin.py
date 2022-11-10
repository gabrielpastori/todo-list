from django.contrib import admin
from .models import Group, Task

admin.site.register(Task)
admin.site.register(Group)