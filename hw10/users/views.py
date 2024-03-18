from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotes:base')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:base')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotes:base')

    return render(request, 'users/login.html', context={"form": LoginForm()})


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quotes:base')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:base')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})
