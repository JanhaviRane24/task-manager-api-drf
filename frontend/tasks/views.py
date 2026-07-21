import requests
from django.shortcuts import render, redirect
from django.contrib import messages

def dashboard(request):

    if "access" not in request.session:
        return redirect("login")

    headers = {
        "Authorization": f"Bearer {request.session['access']}"
    }

    response = requests.get(
        "http://127.0.0.1:8000/api/",
        headers=headers
    )

    if response.status_code == 200:
        tasks = response.json()
    else:
        tasks = []

    return render(
        request,
        "dashboard.html",
        {
            "tasks": tasks
        }
    )

def register_view(request):

    if request.method == "POST":

        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }

        response = requests.post(
            "http://127.0.0.1:8000/api/register/",
            json=data
        )

        print("STATUS:", response.status_code)
        print("DATA:", response.text)

        if response.status_code == 201:
            messages.success(
                request,
                "Registration successful."
            )
            return redirect("login")

        messages.error(
            request,
            response.text
        )

    return render(request, "register.html")

def login_view(request):

    if request.method == "POST":

        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        response = requests.post(
            "http://127.0.0.1:8000/api/login/",
            json=data
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 200:

            tokens = response.json()

            request.session["access"] = tokens["access"]
            request.session["refresh"] = tokens["refresh"]

            messages.success(
                request,
                "Login successful"
            )

            return redirect("dashboard")

        else:
            messages.error(
                request,
                "Invalid username or password"
            )

    return render(request, "login.html")



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