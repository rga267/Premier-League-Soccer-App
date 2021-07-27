from django.urls import path
from . import views 

app_name ='users'

urlpatterns = [
    path('', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('users/', views.home, name="home"),

]