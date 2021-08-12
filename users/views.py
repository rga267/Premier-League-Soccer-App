from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decouple import config
import requests


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
            messages.success(request, 'Account was successfully created for ' + user_name+'.' + ' You can log in now!')
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
    
    search_result = {}

    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    query = {"season":"2020","league":"39"}

    headers = {
    'x-rapidapi-key': config('RAPID_API_KEY'),
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=query)

    if response.status_code == 200:  # SUCCESS
        search_result = response.json()
        search_result['success'] = True
        search_result['rate'] = {
            'limit': response.headers['x-ratelimit-requests-limit'],
            'remaining': response.headers['x-ratelimit-requests-remaining'],
        }
    else:
        search_result['success'] = False
        if response.status_code == 404:  # NOT FOUND
            search_result['message'] = 'API-FOOTBALL services are not available at the moment. Please try again later.'

    context = {'search_result': search_result}
    return render(request, 'users/home.html', context)