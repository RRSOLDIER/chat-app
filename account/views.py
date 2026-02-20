from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import User

def register_view(request):
    if request.method=='POST':
        email = request.POST['email']
        username=request.POST['username']
        password=request.POST['password']

        user= User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        login(request,user)
        return redirect('user_list')
    return render(request,'register.html')


def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request, username=username, password=password)

        if user:
            login(request,user)
            return redirect('user_list')

    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')