import requests
from django.shortcuts import render, redirect

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

    if request.method == "POST":

        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "status": request.POST.get("status"),
            "priority": request.POST.get("priority"),
            "due_date": request.POST.get("due_date"),
        }

        response = requests.post(
            "http://127.0.0.1:8000/api/",
            data=data
        )

        if response.status_code == 201:
            return redirect("dashboard")


    return render(request, "add_task.html")

def edit_task(request, task_id):
    pass

def delete_task(request, task_id):
    pass