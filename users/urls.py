from django.urls import path
from . import views 

app_name ='users'

urlpatterns = [
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('users/', views.home, name="home"),
    path('users/matches', views.matches, name="matches"),
    path('users/favorites', views.favorites, name="favorites"),

]
