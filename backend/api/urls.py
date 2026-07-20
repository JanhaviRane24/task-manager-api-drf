from django.urls import path
from . import views


urlpatterns = [
    path("", views.get_tasks, name="get_tasks"),
    path("update/<int:id>/", views.update_task, name="update_task"),
    path("delete/<int:id>/", views.delete_task, name="delete_task")
]