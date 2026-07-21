import requests
from django.shortcuts import render, redirect
from django.contrib import messages

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

def update_task(request, task_id):

    if request.method == "POST":

        data = {
            "title": request.POST.get("title"),
            "description": request.POST.get("description"),
            "status": request.POST.get("status"),
            "priority": request.POST.get("priority"),
            "due_date": request.POST.get("due_date"),
        }

        response = requests.put(
            f"http://127.0.0.1:8000/api/update/{task_id}/",
            data=data
        )

        if response.status_code == 200:
            return redirect("dashboard")


    response = requests.get(
        "http://127.0.0.1:8000/api/"
    )

    tasks = response.json()

    task = None

    for t in tasks:
        if t["id"] == task_id:
            task = t
            break


    return render(
        request,
        "edit_task.html",
        {
            "task": task
        }
    )

def delete_task(request, task_id):

    if request.method == "POST":

        response = requests.delete(
            f"http://127.0.0.1:8000/api/delete/{task_id}/"
        )

        if response.status_code == 204:
            return redirect("dashboard")

    return redirect("dashboard")