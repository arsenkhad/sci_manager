import requests
from enum import Enum
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from django.http import HttpRequest

from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from account.models import CustomUser

class RequestType(Enum):
    GET = 0
    POST = 1
    PATCH = 2
    DELETE = 3


def get_users_data(users : list[dict]):
    user_ids = [user.get('user_id', None) for user in users]
    user_accsesses = {user.get('user_id', None) : user.get('user_access', None) for user in users}
    users_data = [{'id' : user.user_id, 'username' : user.username, 'full_name' : user.get_full_name(), 'short_name' : user.get_short_name(), 'access' : user_accsesses.get(user.user_id, 0)} for user in CustomUser.objects.filter(user_id__in=user_ids)]
    users_data.sort(key=lambda x: (3 - x['access'], x['full_name']))
    return users_data

def extend_project_data(project : dict):
    project['project_created'] = make_aware(parse_datetime(project.get('project_created')))
    project['project_updated'] = make_aware(parse_datetime(project.get('project_updated')))
    user_id = project.pop('project_author', None)
    if user_id:
        user = CustomUser.objects.get(user_id=user_id)
        if user:
            project['author_login'] = user.username
            project['author_fullname'] = user.get_full_name()
            project['author_shortname'] = user.get_short_name()
    return project


def is_ajax(request : HttpRequest) -> bool:
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def request_router(request : HttpRequest, request_type : RequestType, url, params, payload):
    token = request.session.get('api_token', None)
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    response = None
    if request_type == RequestType.GET:
        response = requests.get(url, params=params, headers=headers)
    elif request_type == RequestType.POST:
        response = requests.post(url, params=params, json=payload, headers=headers)
    elif request_type == RequestType.PATCH:
        response = requests.patch(url, params=params, json=payload, headers=headers)
    elif request_type == RequestType.DELETE:
        response = requests.delete(url, params=params, headers=headers)
    if response == None:
        raise ValueError
    return response


def create_access_token(user_id: int | str, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = {"sub": str(user_id)}
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALG)
    return access_token


# Unused because passwords are stored hashed 
def auth_request(request : HttpRequest):
    auth_url = f'{settings.API_URL}/auth'
    data = {'username': request.user.username, 'password': request.user.password}
    response = requests.post(auth_url, data=data)

    if response.status_code == 200:
        token = response.json().get('access_token')
        request.session['api_token'] = token
        print(type(token), token)
        return True
    else:
        print("Authentication failed")
        return False


def api_request(request : HttpRequest, request_url, request_type : RequestType = RequestType.GET, params=None, payload=None, tries = 0):
    url = settings.API_URL + request_url
    response = request_router(request, request_type, url, params, payload)
    if response.status_code == requests.codes.ok:
        return response.json()
    elif response.status_code == requests.codes.unauthorized and tries < settings.API_REQUEST_MAX_TRIES:
        request.session['api_token'] = create_access_token(request.user.user_id, timedelta(minutes=settings.TOKEN_EXPIRE))
        return api_request(request, request_url, request_type, params, payload, tries+1)
    else:
        return None


# def api_request(request_type : RequestType, url, params=None, payload=None):
#     def decorator(function):
#         def wrapper(*args, **kwargs):
#             response = request_handler(request_type, url, params, payload)
#             return function(*args, **kwargs, response=response)
#         return wrapper
#     return decorator
