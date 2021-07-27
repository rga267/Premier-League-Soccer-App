from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.
def signup(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created for ' + user_name+'.' + 'You can log in now!')
            return redirect('login')

    context = {'form':form}
    return render(request, 'users/signup.html', context)

def login(request):
    context = {}
    return render(request, 'users/login.html', context)

def home(request):
    context = {}
    return render(request, 'users/home.html', context)