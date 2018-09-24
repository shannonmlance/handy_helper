from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard),
    url(r'^addJob$', views.addJob),
    url(r'^createJob$', views.createJob),
    url(r'^destroy/(?P<id>\d+)$', views.destroy),
    url(r'^edit/(?P<id>\d+)$', views.editJob),
    url(r'^update/(?P<id>\d+)$', views.updateJob),
    url(r'^view/(?P<id>\d+)$', views.viewJob),
    url(r'^join/(?P<id>\d+)$', views.joinJob), # remember to add commas!
]