import requests
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages



API_URL = "http://127.0.0.1:8000/api/"

def refresh_access_token(request):
    refresh_token = request.session.get("refresh")

    if not refresh_token:
        return None

    response = requests.post(
        API_URL + "refresh/",
        data={"refresh": refresh_token}
    )

    if response.status_code == 200:
        new_access = response.json()["access"]
        request.session["access"] = new_access
        return new_access

    return None
def home(request):
    return redirect("login")

def api_request(request, method, url, **kwargs):
    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {request.session.get('access')}"

    response = requests.request(method, url, headers=headers, **kwargs)

    if response.status_code == 401:
        new_access = refresh_access_token(request)

        if new_access:
            headers["Authorization"] = f"Bearer {new_access}"
            response = requests.request(method, url, headers=headers, **kwargs)
        else:
            return None

    return response

def dashboard(request):

    if "access" not in request.session:
        return redirect("login")

    response = api_request(request, "GET", API_URL)

    if response is None:
        return redirect("login")

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
            API_URL + "register/",
            json=data
        )


        if response.status_code == 201:

            messages.success(
                request,
                "Registration successful"
            )

            return redirect("login")


        else:

            messages.error(
                request,
                response.text
            )


    return render(
        request,
        "register.html"
    )






def login_view(request):


    if request.method == "POST":


        data = {

            "username": request.POST.get("username"),
            "password": request.POST.get("password"),

        }


        response = requests.post(
            API_URL + "login/",
            data=data
        )


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



    return render(
        request,
        "login.html"
    )







def logout_view(request):

    request.session.flush()

    return redirect("login")









def add_task(request):

    if "access" not in request.session:

        return redirect("login")



    if request.method == "POST":


        data = {


            "title": request.POST.get("title"),

            "description": request.POST.get("description"),

            "status": request.POST.get("status"),

            "priority": request.POST.get("priority"),

            "due_date": request.POST.get("due_date"),

        }



        response = api_request(request, "POST", API_URL, json=data)

        if response is None:
            return redirect("login")


        if response.status_code == 201:

            return redirect("dashboard")



    return render(
        request,
        "add_task.html"
    )














    # UPDATE TASK

def update_task(request, task_id):

    if "access" not in request.session:
        return redirect("login")


    headers = {
        "Authorization": f"Bearer {request.session['access']}"
    }


    if request.method == "POST":

        data = {

            "title": request.POST.get("title"),

            "description": request.POST.get("description"),

            "status": request.POST.get("status"),

            "priority": request.POST.get("priority"),

            "due_date": request.POST.get("due_date"),

        }


        response = api_request(
            request, "PUT",
            f"{API_URL}update/{task_id}/",
            json=data
        )

        if response is None:
            return redirect("login")

        if response.status_code == 200:
            return redirect("dashboard")



    # get task details for edit form

    response = api_request(request, "GET", API_URL)

    if response is None:
        return redirect("login")


    tasks = response.json()

    task = None


    if isinstance(tasks, list):

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


    if "access" not in request.session:

        return redirect("login")



    if request.method == "POST":


        response = api_request(
            request, "DELETE",
            f"{API_URL}delete/{task_id}/"
        )

        if response is None:
            return redirect("login")



        if response.status_code == 204:

            return redirect("dashboard")



    return redirect("dashboard")


