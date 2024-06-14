from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^projects/(?P<project_id>\d+)/edit', views.editor, name='project-edit'),
    re_path(r'^projects/(?P<project_id>\d+)/users', views.project_users, name='project-users'),
    re_path(r'^projects/(?P<project_id>\d+)/graph', views.graph, name='graph'),
    re_path(r'^projects/(?P<project_id>\d+)', views.project, name='project'),
    re_path(r'^projects/add', views.projects_add, name='projects-add'),
    re_path(r'^projects', views.projects, name='projects'),
    path('', views.projects, name='main'),
    # path('projects/add', views.projectsAdd, name='projects-add'),
]