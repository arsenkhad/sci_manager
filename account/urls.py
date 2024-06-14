from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.auth, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.create_acc, name='create_account'),
    path('profile/', views.profile, name='profile'),
]