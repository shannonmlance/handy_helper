from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

# these are the methods that are run by the corresponding urls

# called by "/" through url(r'^$', views.index)
def index(request):
    request.session.clear()
    return render(request, "login_app/login.html")

# called by "/register" through url(r'^register$', views.register)
def register(request):
    # if the page is accessed through POST
    if request.method == "POST":
        # load the errors
        errors=User.objects.basic_validator(request.POST)
        # if there are any errors
        if len(errors):
            # display them
            for key, value in errors.items():
                messages.error(request, value)
            # and redirect back from which page the POST came
            return redirect("/")
        # otherwise, if the POSTed email matches an email already registered
        elif User.objects.filter(email=request.POST["email"]):
            # display an error
            messages.error(request, "Email is already registered.")
            # and redirect back from which page the POST came
            return redirect("/")
        # otherwise
        else:
            # hash and salt the POSTed password
            pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            # capture all of the POSTed information (remember to decode the pw before saving it)
            registered = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=pw_hash.decode())
            # store some useful information in session
            request.session["name"] = registered.first_name
            request.session["id"] = registered.id
            # and redirect to the belt exam app
            return redirect("/dashboard")
    # otherwise
    else:
        # redirect back from which page the POST came
        return redirect("/")

# called by "/login" through url(r'^login$', views.login)
def login(request):
    # if the page is accessed through POST
    if request.method == "POST":
        # find all emails in the database that match the POSTed email and store that list in a variable
        logged = User.objects.filter(email=request.POST["email"])
        # if the list is empty
        if len(logged) == 0:
            # then no matches were found; display an error
            messages.error(request, "Not a valid email.")
            # and redirect back from which page the POST came
            return redirect("/")
        # otherwise, if a matching email was found, check if the password belonging to that email matches the POSTed password
        elif not bcrypt.checkpw(request.POST["password"].encode(), logged[0].password.encode()):
            # if it does not, then display an error
            messages.error(request, "Password is incorrect.")
            # and redirect back from which page the POST came
            return redirect("/")
        # otherwise
        else:
            # store some useful information in session
            request.session["name"] = logged[0].first_name
            request.session["id"] = logged[0].id
            # and redirect to the belt exam app
            return redirect("/dashboard")
    # otherwise
    else:
        # redirect back from which page the POST came
        return redirect("/")
