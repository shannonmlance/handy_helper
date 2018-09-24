from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.login_app.models import User
import bcrypt
from time import localtime, strftime
from .models import Job


# these are the methods that are run by the corresponding urls

# called by "/dashboard" through url(r'^dashboard$', views.dashboard)
def dashboard(request):
    # if the page is not accessed through the login app
    if "id" not in request.session:
        # redirect back to the login page
        return redirect("/")
    # otherwise
    else:
        print("at the dashboard")
        # add context
        context = {
            "jobs" : Job.objects.all()
        }
        # render the dashboard page
        return render(request, "belt_app/dashboard.html", context)

# called by "/addJob" through url(r'^addJob$', views.addJob)
def addJob(request):
    # if the page is not accessed from the dashboard
    if "id" not in request.session:
        # redirect back to the login page
        return redirect("/")
    # otherwise
    else:
        print("ready to add a job")
        # render the addJob page
        return render(request, "belt_app/addJob.html")

# called by "/createJob" through url(r'^createJob$', views.createJob)
def createJob(request):
    # if the page is accessed by POST
    if request.method == "POST":
        print("received via post", request.POST)
        # load the errors
        errors = Job.objects.basic_validator(request.POST)
        # if there are any errors
        if len(errors):
            # display them
            for key, value in errors.items():
                messages.error(request, value)
            # and redirect back to the page from which the POST came
            return redirect("/addJob")
        # otherwise
        else:
            print("post is valid", request.POST)
            # create the job
            Job.objects.create(title=request.POST["title"], description=request.POST["description"], location=request.POST["location"], user_posted=User.objects.get(id=request.session["id"]), user_worked=User.objects.get(id=1))
            # and redirect back to the dashboard
            return redirect("/dashboard")
    # otherwise
    else:
        # redirect back to the addJob page
        return redirect("/addJob")

# called by "/view/<id>" through url(r'^view/(?P<id>\d+)$', views.viewJob)
def viewJob(request, id):
    # if the page is not accessed from the dashboard
    if "id" not in request.session:
        # redirect back to the login page
        return redirect("/")
    # otherwise
    else:
        print("look at this job")
        context = {
            "jobs" : Job.objects.get(id=id)
        }
        # render the viewJob page
        return render(request, "belt_app/viewJob.html", context)

# called by "/edit/<id>" through url(r'^edit/(?P<id>\d+)$', views.editJob)
def editJob(request, id):
    # if the page is not accessed from the dashboard
    if "id" not in request.session:
        # redirect back to the login page
        return redirect("/")
    # otherwise
    else:
        print("ready to edit job")
        context = {
            "jobs" : Job.objects.get(id=id)
        }
        # render the editJob page
        return render(request, "belt_app/editJob.html", context)

# called by "/update/<id>" through url(r'^update/(?P<id>\d+)$', views.updateJob)
def updateJob(request, id):
    # if the page is accessed by POST
    if request.method == "POST":
        print("udpate received via post", request.POST)
        # load the errors
        errors = Job.objects.basic_validator(request.POST)
        # if there are any errors
        if len(errors):
            # display them
            for key, value in errors.items():
                messages.error(request, value)
            # and redirect back to the page from which the POST came
            up = Job.objects.get(id=id)
            return redirect("/edit/"+str(up.id))
        # otherwise
        else:
            print("update is valid", request.POST)
            # update the job
            up = Job.objects.get(id=id)
            up.title = request.POST["title"]
            up.description = request.POST["description"]
            up.location = request.POST["location"]
            up.save()
            # and redirect back to the dashboard
            return redirect("/dashboard")
    # otherwise
    else:
        up = Job.objects.get(id=id)
        # redirect back to the addJob page
        return redirect("/edit/"+str(up.id))

# called by "/join/<id>" through url(r'^join/(?P<id>\d+)$', views.joinJob)
def joinJob(request, id):
    # if the page is not accessed from the dashboard
    if "id" not in request.session:
        # redirect to login page
        return redirect("/")
    # otherwise
    else:
        # update the job with the new join
        j = Job.objects.get(id=id)
        j.user_worked = User.objects.get(id=request.session["id"])
        j.save()
        print(j.user_worked, "has been updated")
        # redirect to the dashboard
        return redirect("/dashboard")

# called by "/destroy/<id>" through url(r'^destroy/(?P<id>\d+)$', views.destroy)
def destroy(request, id):
    # if the page is not accessed from the dashboard
    if "id" not in request.session:
        # redirect to login page
        return redirect("/")
    # otherwise
    else:
        # delete the information from the database
        x = Job.objects.get(id=id)
        print(x, "will be deleted")
        x.delete()
        # and return to the dashboard
        return redirect("/dashboard")
