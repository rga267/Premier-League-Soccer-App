from django.urls import path
from . import views 

app_name ='users'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    
    path('', views.home, name="home"),

]