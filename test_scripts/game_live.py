import os
import requests
from dotenv import load_dotenv
import json

def get_game_state(team_abbreviation):
    load_dotenv()  # finds and reads .env in the current directory

    url = "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

    response = requests.request("GET", url)

    data = response.json()

    
    for event in data['events']:
        for competitors in event['competitions'][0]['competitors']:
            team = competitors['team']['abbreviation']
            if team == team_abbreviation:
                status = event['competitions'][0]['status']['type']['state']
                return status

# print(get_game_state('MIL'))