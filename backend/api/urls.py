from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login_view, name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
   
    path("", views.get_tasks),
    path("update/<int:id>/", views.update_task),
    path("delete/<int:id>/", views.delete_task),
]