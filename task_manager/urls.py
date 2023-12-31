from django.urls import path

from task_manager.views import (
    index,
    SignUpView,
    TeamListView,
    UserTeamListView,
    TeamCreateView,
    TeamDetailView,
    TeamUpdateView,
    AssignUserToTeamView,
    RemoveUserFromTeamView,
    TaskListView,
    UserTaskListView,
    TaskDetailView,
    TaskUpdateView,
    TaskCreateView,
    TaskDeleteView,
    AssignUserToTaskView,
    AddCommentView,
    CommentaryDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("teams/", TeamListView.as_view(), name="team-list"),
    path("user/teams/", UserTeamListView.as_view(), name="user-team-list"),
    path("teams/create/", TeamCreateView.as_view(), name="teams-create"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/assign/", AssignUserToTeamView.as_view(), name="assign-user"),
    path(
        "teams/<int:pk>/delete/", RemoveUserFromTeamView.as_view(), name="delete-user"
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("user/tasks/", UserTaskListView.as_view(), name="user-task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/assign/", AssignUserToTaskView.as_view(), name="take-to-work"),
    path(
        "tasks/<int:pk>/add_comment/", AddCommentView.as_view(), name="task-add-comment"
    ),
    path(
        "commentary/<int:pk>/delete/",
        CommentaryDeleteView.as_view(),
        name="commentary-delete",
    ),
]

app_name = "task_manager"
