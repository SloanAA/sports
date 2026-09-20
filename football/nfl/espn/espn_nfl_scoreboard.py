import os
import requests
from dotenv import load_dotenv
import json

def get_team_score():
    load_dotenv()  # finds and reads .env in the current directory

    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

    response = requests.request("GET", url)

    data = response.json()

    # print(json.dumps(data))  # Print the entire JSON response for debugging
    for event in data['events']:
        for competitors in event['competitions'][0]['competitors']:
            team = competitors['team']['abbreviation']
            print(team)

# team_abbreviation = 'CHC'  # Example team abbreviation
# get_team_score('NYY')
get_team_score()  # Example team abbreviation for New England Patriots