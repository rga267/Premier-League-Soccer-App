from django.shortcuts import render

# Create your views here.
def signup(request):
    context = {}
    return render(request, 'users/signup.html', context)

def login(request):
    context = {}
    return render(request, 'users/login.html', context)

def home(request):
    context = {}
    return render(request, 'users/home.html', context)