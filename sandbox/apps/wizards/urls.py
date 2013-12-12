
from django.conf.urls import patterns, url

from sandbox.apps.wizards import views

urlpatterns = patterns('',
    url(r'^$', views.TaskView.as_view(), name='task')
)

