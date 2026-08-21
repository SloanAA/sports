from dotenv import load_dotenv
import json
import requests

def get_game_summary(team_abbreviation):
    load_dotenv()  # finds and reads .env in the current directory

    url = "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

    response = requests.request("GET", url)

    data = response.json()

    
    # for event in data['events']:
    #     for competitors in event['competitions'][0]['competitors']:
    #         team = competitors['team']['abbreviation']
    #         if team == team_abbreviation:
    #             final_score = competitors['score']
    #             hits = competitors['hits']
    #             return final_score, hits

    for event in data['events']:
        competitions = event['competitions'][0]
        teams = competitions['competitors']  # list of 2 teams

        abbrs = [c['team']['abbreviation'] for c in teams]
        if team_abbreviation in abbrs:
            for competitors in teams:
                team = competitors['team']['abbreviation']
                score = competitors['score']
                hits = competitors['hits']
                errors = competitors['errors']
                records = competitors['records'][0]['summary']
                if team == team_abbreviation:
                    my_score = score
                    my_hits = hits
                    my_errors = errors
                    my_records = records
                else:
                    opponent = team
                    opponent_score = score
                    opponent_hits = hits
                    opponent_errors = errors
                    opponent_records = records
            return team_abbreviation, my_score, my_hits, my_errors, my_records, opponent, opponent_score, opponent_hits, opponent_errors, opponent_records

# team_abbreviation = "MIL"  # Example team abbreviation
# team, my_score, my_hits, my_errors, my_records, opponent, opponent_score, opponent_hits, opponent_errors, opponent_records = get_game_summary(team_abbreviation)

# print(f"         Runs    Hits    Errors")
# print(f"{team}      {my_score}       {my_hits}       {my_errors}         ({my_records})")
# print(f"{opponent}      {opponent_score}       {opponent_hits}       {opponent_errors}         ({opponent_records})")
