from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decouple import config
from operator import itemgetter
from .models import Team
import requests
import datetime
import json 
import pdb; 

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


#store teams info in database from first call
@login_required(login_url='users:login')
def home(request):
    
    search_result = {}

    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    query = {"season":"2021","league":"39"}
    #add dynamic season entry functionality

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

#clean up this code when done i.e. use js_string and rename to search_result
@login_required(login_url='users:login')
def matches(request):
    
    search_result = {}

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    query = {"league":"39","season":"2021","from":"2021-08-12","to":"2021-11-01"} 

    headers = {
    'x-rapidapi-key': config('RAPID_API_KEY'),
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=query)

    js_string = json.loads(response.text)

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
    
    for times in js_string['response']:
        time_obj = datetime.datetime.strptime(times['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
        time_time = time_obj.time()
        time_date = time_obj.date()
        times['date'] = time_date.strftime("%A, %B %d, %Y")
        times['time'] = time_time.strftime("%-I:%M %p")

    js_string['response'] = sorted(js_string['response'], key=lambda k: k['fixture']['date'])

    context = {'search_result': search_result, "js_string": js_string}
    return render(request, 'users/matches.html', context)


@login_required(login_url='users:login')
def favorites(request):

    search_result = {}

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    query = {"league":"39","season":"2021","from":"2021-08-12","to":"2021-11-01"} 
    
    headers = {
    'x-rapidapi-key': config('RAPID_API_KEY'),
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=query)

    js_string_fav = json.loads(response.text)

    user_team_ids = list(request.user.favorites.teams.all().values_list('team_id', flat=True))

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


    for times in js_string_fav['response']:
   
        time_obj = datetime.datetime.strptime(times['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
        time_time = time_obj.time()
        time_date = time_obj.date()
        times['date'] = time_date.strftime("%A, %B %d, %Y")
        times['time'] = time_time.strftime("%-I:%M %p")
    

    js_string_fav['response'] = sorted(js_string_fav['response'], key=lambda k: k['fixture']['date'])


    for items in js_string_fav['response'][:]:
        if items['teams']['home']['id'] not in user_team_ids and items['teams']['away']['id'] not in user_team_ids:
            js_string_fav['response'].remove(items)
    
    context = {'search_result': search_result, "js_string_fav": js_string_fav}
    return render(request, 'users/favorites.html', context)


@login_required(login_url='users:login')
def editfavorites(request):

    user = request.user
    current_teams = list(user.favorites.teams.all().values_list('team_id', flat=True))

    if request.method == "POST":
        data = request.POST.values()
        selected_ids = list(data)

        for x in current_teams:
            if x not in selected_ids:
                team = Team.objects.get(team_id=x)
                user.favorites.teams.remove(team)
                user.save()

        for x in selected_ids[1:]:
            if x not in current_teams:
                team = Team.objects.get(team_id=x)
                user.favorites.teams.add(team)
                user.save()

        return redirect('users:favorites')

    all_teams = Team.objects.all()
    context = {'all_teams': all_teams, 'current_teams': current_teams}
    return render(request, 'users/editfavorites.html', context)

