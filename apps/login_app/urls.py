from django.conf.urls import url
from . import views

# this is linked from the project's urls.py file
# match a url using the r'^$'
# go to the appropriate views (methods)

urlpatterns= [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login), # remember to add commas!
]