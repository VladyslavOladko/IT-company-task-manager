from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from task_manager.foms import (
    SignUpForm,
    TeamForm,
    TaskForm,
    TaskStatusForm,
    TeamSearchForm,
    CommentForm, TaskNeedHelpForm
)

from task_manager.models import (
    Team,
    Employee,
    Task,
    Commentary,
)


def index(request):

    num_teams = Team.objects.all().count
    num_users = Employee.objects.all().count
    is_home_page = True

    context = {
        "num_teams": num_teams,
        "num_users": num_users,
        "is_home_page": is_home_page,
    }

    return render(request, "task_manager/index.html", context=context)


class SignUpView(generic.CreateView):

    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("task_manager:team-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class TeamListView(LoginRequiredMixin, generic.ListView):

    model = Team
    template_name = "task_manager/team_list.html"
    context_object_name = "team_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TeamSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Team.objects.prefetch_related("teammates")
        form = TeamSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class UserTeamListView(LoginRequiredMixin, generic.ListView):

    model = Team
    template_name = "task_manager/user_team_list.html"
    paginate_by = 10


class TeamCreateView(LoginRequiredMixin, generic.CreateView):

    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task_manager:team-list")
    template_name = "task_manager/team_form.html"


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Team
    form_class = TeamForm
    template_name = "task_manager/team_form.html"


class TeamDetailView(LoginRequiredMixin, generic.DetailView):

    model = Team
    form_class = TeamForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["is_user_teammate"] = self.object.teammates.filter(
            id=self.request.user.id
        ).exists()
        return context


class AssignUserToTeamView(LoginRequiredMixin, generic.View):

    @staticmethod
    def post(request, pk):
        team = get_object_or_404(Team, pk=pk)
        if request.user.is_authenticated:
            team.teammates.add(request.user)
        return redirect("task_manager:team-detail", pk=pk)


class RemoveUserFromTeamView(LoginRequiredMixin, generic.View):

    @staticmethod
    def post(request, pk):
        team = get_object_or_404(Team, pk=pk)
        if request.user.is_authenticated:
            team.teammates.remove(request.user)
        return redirect("task_manager:team-detail", pk=pk)


class TaskListView(LoginRequiredMixin, generic.ListView):

    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get(self, request):
        user = request.user
        user_teams = user.teams.all()
        tasks = Task.objects.filter(team__in=user_teams)

        context = {
            'tasks': tasks
        }

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["assignee"] = self.request.user
        context["task_need_help_form"] = TaskNeedHelpForm()
        context["task_status_form"] = TaskStatusForm()
        return context

    def post(self, request, *args, **kwargs):
        is_need_help_task_id = request.POST.get("is_need_help_task_id")
        is_completed_task_id = request.POST.get("is_completed_task_id")

        if is_need_help_task_id:
            task = Task.objects.get(id=is_need_help_task_id)
            task.is_need_help = not task.is_need_help
            task.save()

        if is_completed_task_id:
            task = Task.objects.get(id=is_completed_task_id)
            task.is_completed = not task.is_completed
            task.save()

        return redirect("task_manager:task-list")


class UserTaskListView(LoginRequiredMixin, generic.ListView):

    model = Task
    template_name = "task_manager/user_task_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["assignee"] = self.request.user
        context["task_need_help_form"] = TaskNeedHelpForm()
        context["task_status_form"] = TaskStatusForm()
        return context

    def post(self, request, *args, **kwargs):
        is_need_help_task_id = request.POST.get("is_need_help_task_id")
        is_completed_task_id = request.POST.get("is_completed_task_id")

        if is_need_help_task_id:
            task = Task.objects.get(id=is_need_help_task_id)
            task.is_need_help = not task.is_need_help
            task.save()

        if is_completed_task_id:
            task = Task.objects.get(id=is_completed_task_id)
            task.is_completed = not task.is_completed
            task.save()

        return redirect("task_manager:user-task-list")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):

    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["is_user_assignee"] = \
            self.object.assignees.filter(id=self.request.user.id).exists()
        context["task_status_form"] = TaskStatusForm()
        return context

    def post(self, request, *args, **kwargs):
        task_id = self.kwargs["pk"]
        task = Task.objects.get(id=task_id)
        task.is_completed = not task.is_completed
        task.save()
        return redirect("task_manager:task-detail", pk=task_id)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):

    model = Task
    form_class = TaskForm


class TaskCreateView(LoginRequiredMixin, generic.CreateView):

    model = Task
    form_class = TaskForm


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):

    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")


class AssignUserToTaskView(LoginRequiredMixin, generic.View):

    @staticmethod
    def post(request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user.is_authenticated:
            task.assignees.add(request.user)
        return redirect("task_manager:task-detail", pk=pk)


class AddCommentView(LoginRequiredMixin, generic.CreateView):
    def post(self, request, *args, **kwargs):
        task_id = kwargs["pk"]
        task_url = reverse("task_manager:task-detail", kwargs={"pk": task_id})
        form = CommentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["content"]

            if task_id and content:
                form.instance.user_id = self.request.user.pk
                form.instance.task_id = task_id
                self.success_url = task_url
                return super().form_valid(form)

        return HttpResponseRedirect(task_url)


class CommentaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Commentary
    template_name = "task_manager/commentary_confirm_delete.html"

    def get_success_url(self):
        commentary = self.get_object()
        task_id = commentary.task.id
        task_url = reverse("task_manager:task-detail", kwargs={"pk": task_id})
        return task_url

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
