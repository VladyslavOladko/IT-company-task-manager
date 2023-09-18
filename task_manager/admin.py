from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import (
    Employee,
    Position,
    Team,
    Task,
    TaskType,
)


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (("Position", {"fields": ("position",)}),)


admin.site.register(Position)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(TaskType)
