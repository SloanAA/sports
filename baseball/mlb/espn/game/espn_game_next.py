from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def get_opponent(matchup, team_abbreviation):
    away, home = matchup.split(" @ ")
    return home if away == team_abbreviation else away


def get_game_next(team_abbreviation):
    load_dotenv()

    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/{team_abbreviation}/schedule"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    now = datetime.now(timezone.utc)

    upcoming = []
    for event in data["events"]:
        event_time = datetime.fromisoformat(event["date"].replace("Z", "+00:00"))
        status_state = event["competitions"][0]["status"]["type"]["state"]

        if event_time > now and status_state == "pre":
            upcoming.append((event_time, event))

    if not upcoming:
        return None

    upcoming.sort(key=lambda x: x[0])
    next_time, next_event = upcoming[0]

    eastern_time = next_time.astimezone(ZoneInfo("America/New_York"))



    matchup = next_event["shortName"]
    shortDetail = next_event["competitions"][0]["status"]["type"]["shortDetail"]

    return matchup, eastern_time, shortDetail

    # {
    #     "matchup": next_event["shortName"],
    #     "date_utc": next_time.isoformat(),
    #     "shortDetail": next_event["competitions"][0]["status"]["type"]["shortDetail"],
    # }


# print(json.dumps(get_next_game_start("CHC")))