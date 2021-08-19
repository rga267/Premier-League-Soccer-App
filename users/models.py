from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Team(models.Model):
    name = models.CharField(max_length=100, null=True)
    team_id = models.CharField(max_length=100, null=True)
    logo = models.URLField(null=True)
    #user = models.ManytoManyField(settings.AUTH_USER_MODEL, through='Favorites')

    def __str__(self):
        return self.name

'''
class FavoritesManager(models.Manager):
    use_for_related_fields = True

    def add_team(self, user, team):
        

    def remove_team(self, user, team):
        
'''
class Favorites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    #teams = models.ForeignKey(Team, on_delete=models.CASCADE)

    #objects = models.Manager()
    #fav_objects = FavoritesManager()

    def __str__(self):
        return self.user.username
