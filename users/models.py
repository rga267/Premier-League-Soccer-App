from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Team(models.Model):
    name = models.CharField(max_length=100, null=True)
    team_id = models.IntegerField(null=True)
    logo = models.URLField(null=True)

    def __str__(self):
        return self.name

class Favorites(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.user.username
