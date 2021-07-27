from django.shortcuts import render

# Create your views here.
def signUp(request):
    context = {}
    return render(request, 'users/signup.html', context)

