from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("add/", views.add_task, name="add_task"),
    path("update/<int:task_id>/", views.update_task, name="update_task"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
]