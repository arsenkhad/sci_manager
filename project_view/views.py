from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.template import loader
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
import json

from .utils import is_ajax, RequestType, api_request, extend_project_data, get_users_data


@login_required
def projects(request : HttpRequest):
    if is_ajax(request):
        projects : dict = api_request(request, '/project/info')
        if projects:
            projects = projects.get('projects', None)
        for project in projects:
            extend_project_data(project)
        return render(request, 'projects/project_list.html', {"projects" : projects})
    return render(request, 'main.html')


@login_required
def project(request : HttpRequest, project_id : int):
    if is_ajax(request):
        api_response : dict = api_request(request, f'/project/{project_id}')
        if not api_response:
            return HttpResponseBadRequest("Project wasn't found.")
        project = api_response.get('project', None)
        access = api_response.get('access', None)
        extend_project_data(project)
        return render(request, 'projects/project_info.html', {"project" : project, "access_level" : access})

    return render(request, 'projects/project.html', {'project_id' : project_id})


@login_required
def graph(request : HttpRequest, project_id : int):
    if is_ajax(request):
            project_graph = api_request(request, f'/project/{project_id}/graph')
            return render(request, 'projects/graph_view.html', {"graph" : json.dumps(project_graph)})
    return redirect('project', project_id=project_id) 


@login_required
def project_users(request : HttpRequest, project_id : int):
    if is_ajax(request):
        users = api_request(request, f'/project/{project_id}/users')
        if not users:
            return HttpResponseBadRequest("Users weren't found.")

        users_info = get_users_data(users.get('users', None))
        return render(request, 'projects/project_users.html', {"users" : users_info})
    return redirect('project', project_id=project_id)


@login_required
def projects_add(request : HttpRequest):
    if request.method == 'POST':
        pass
    template = loader.get_template('projects/project_new.html')
    return HttpResponse(template.render())


@login_required
def editor(request : HttpRequest, project_id : int):
    template = loader.get_template('projects/project_editor.html')
    return HttpResponse(template.render())