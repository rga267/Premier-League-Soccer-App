from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('users:home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created for ' + user_name+'.' + 'You can log in now!')
            return redirect('users:login')

    context = {'form':form}
    return render(request, 'users/signup.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('users:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('users:home')
        else:
            messages.info(request, 'Username OR password is incorrect!')

    context = {}
    return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('users:login')

@login_required(login_url='users:login')
def home(request):
    context = {}
    return render(request, 'users/home.html', context)