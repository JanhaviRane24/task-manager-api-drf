import requests
from django.shortcuts import render

def dashboard(request):
    response = requests.get("http://127.0.0.1:8000/api/")

    if response.status_code == 200:
        tasks = response.json()
    else:
        tasks = []
    return render(request, "dashboard.html", {"tasks": tasks})

def login_view(request):
    pass
def register_view(request):
    pass

def logout_view(request):
    pass

def add_task(request):
    pass

def edit_task(request, task_id):
    pass

def delete_task(request, task_id):
    pass