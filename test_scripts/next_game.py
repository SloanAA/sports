from dotenv import load_dotenv
import requests
import json

# Current time in Eastern, right now
from datetime import datetime
from zoneinfo import ZoneInfo


# Parsing an ISO string directly
utc_time = datetime.fromisoformat("2026-08-21T20:10:00Z".replace("Z", "+00:00"))
eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))

def get_next_game(team_abbreviation):
    load_dotenv()  # finds and reads .env in the current directory

    url = "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

    response = requests.request("GET", url)

    data = response.json()

    
    for event in data['events']:
        for competitors in event['competitions'][0]['competitors']:
            team = competitors['team']['abbreviation']
            if team == team_abbreviation:
                next_game_time = event['competitions'][0]['date']

                # Current time in Eastern, right now
                # Parsing an ISO string directly
                utc_time = datetime.fromisoformat(next_game_time.replace("Z", "+00:00"))
                eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))
                return eastern_time.strftime("%I:%M %p on %B %d, %Y")  # Format the time in a readable way

# team_abbreviation = "NYY"  # Example team abbreviation
# print(f"Next game for {team_abbreviation} is at {get_next_game(team_abbreviation)}")