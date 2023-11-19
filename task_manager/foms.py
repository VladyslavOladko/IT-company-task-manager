from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Employee, Team, Task, Commentary


class SignUpForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ("username", "email", "first_name", "last_name", "position")


class TeamForm(forms.ModelForm):
    teammates = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Team
        fields = ("name",)


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by team`s name..."}),
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "team")
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class TaskStatusForm(forms.Form):
    is_completed = forms.BooleanField(required=False, widget=forms.HiddenInput())


class TaskNeedHelpForm(forms.Form):
    is_need_help = forms.BooleanField(required=False, widget=forms.HiddenInput())


class CommentForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["content"]
