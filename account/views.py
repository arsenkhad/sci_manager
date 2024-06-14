from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def create_acc(request):
    return redirect('auth') 

def auth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_page = request.GET.get('next', '/projects')
                    return redirect(next_page)
                else:
                    return render(request, 'auth/auth.html', {'form': form, 'message' : 'Аккаунт недействителен'})
            else:
                return render(request, 'auth/auth.html', {'form': form, 'message' : 'Неверный логин или пароль'})
    else:
        form = LoginForm()
    return render(request, 'auth/auth.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('main') 

def profile(request):
    return redirect('main') 
