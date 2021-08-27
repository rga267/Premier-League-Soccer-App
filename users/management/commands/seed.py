from django.core.management.base import BaseCommand, CommandError   
from users.models import Team
import requests
import json
from decouple import config


def clear_data():
   Team.objects.all().delete()

def get_teams():

    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    query = {"season":"2021","league":"39"}

    headers = {
    'x-rapidapi-key': config('RAPID_API_KEY'),
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers, params=query)

    teams = json.loads(response.text)

    return teams


def seed_teams():
    search_result = get_teams()
    for result in search_result['response']:
        for teams in result['league']['standings']:
            for info in teams:
                team = Team(name=info['team']['name'], team_id=info['team']['id'], logo=info['team']['logo'])
                team.save()



class Command(BaseCommand):
    help = 'Update Team DB'

    def handle(self, *args, **options):
        clear_data()
        seed_teams()
        print("Successfully Updated")