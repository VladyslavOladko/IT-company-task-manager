from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from it_company_task_manager import settings


class TaskType(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Position(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Employee(AbstractUser):

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["first_name"]
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self):
        return f"|{self.username}|  {self.first_name} {self.last_name} ({self.position})"


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    teammates = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("task_manager:team-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):

    PRIORITY = [
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High"),
        ("U", "Urgent"),
        ("C", "Critical"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} to {self.deadline} with {self.priority} priority"

    def get_absolute_url(self):
        return reverse("task_manager:task-detail", args=[str(self.id)])


class Commentary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)

    def __str__(self):
        return f"Comment: {self.content}"
