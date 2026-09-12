from test_scripts.team_specific_score import get_team_score
import time
import threading
from govee.govee_scripts.load_and_save import load_devices, save_devices
from govee.govee_scripts.put_request import rgbLight, colorTempLight
from team_color import get_team_color
from govee.govee_scripts.state_request import get_current_device_colors, DEVICES
from concurrent.futures import ThreadPoolExecutor
from test_scripts.game_live import get_game_state
from test_scripts.game_start import get_game_start
from datetime import datetime
from score_trigger import score_trigger
from test_scripts.game_summary import get_game_summary
from test_scripts.next_game_start import get_next_game_start
import json
import os

import argparse

TEAM_ABBREVIATIONS = {
    "diamondbacks": "ARI", "dbacks": "ARI", "ari": "ARI",
    "braves": "ATL", "atl": "ATL",
    "orioles": "BAL", "bal": "BAL",
    "redsox": "BOS", "bos": "BOS",
    "cubs": "CHC", "chc": "CHC",
    "whitesox": "CHW", "chw": "CHW",
    "reds": "CIN", "cin": "CIN",
    "guardians": "CLE", "cle": "CLE",
    "rockies": "COL", "col": "COL",
    "tigers": "DET", "det": "DET",
    "astros": "HOU", "hou": "HOU",
    "royals": "KC", "kc": "KC",
    "angels": "LAA", "laa": "LAA",
    "dodgers": "LAD", "lad": "LAD",
    "marlins": "MIA", "mia": "MIA",
    "brewers": "MIL", "mil": "MIL",
    "twins": "MIN", "min": "MIN",
    "mets": "NYM", "nym": "NYM",
    "yankees": "NYY", "nyy": "NYY",
    "athletics": "OAK", "oak": "OAK",
    "phillies": "PHI", "phi": "PHI",
    "pirates": "PIT", "pit": "PIT",
    "padres": "SD", "sd": "SD",
    "giants": "SF", "sf": "SF",
    "mariners": "SEA", "sea": "SEA",
    "cardinals": "STL", "stl": "STL",
    "rays": "TB", "tb": "TB",
    "rangers": "TEX", "tex": "TEX",
    "bluejays": "TOR", "tor": "TOR",
    "nationals": "WSH", "wsh": "WSH",
}

def parse_args():
    parser = argparse.ArgumentParser(description="Monitor a team's live score.")
    parser.add_argument("team", help="Team name or abbreviation, e.g. 'yankees' or 'nyy'")
    return parser.parse_args()

def get_selected_team(args):
    key = args.team.lower().replace(" ", "")
    if key not in TEAM_ABBREVIATIONS:
        valid = ", ".join(sorted(set(TEAM_ABBREVIATIONS.keys())))
        raise SystemExit(f"Unknown team '{args.team}'. Valid options:\n{valid}")
    return TEAM_ABBREVIATIONS[key]

def monitor_team_score(team_abbreviation, score_trigger):
    next_call = time.monotonic()
    old_score = 0

    #establish a current state when first running script
    # for location in DEVICES:
    #     state, brightness, color, color_temp = get_current_device_colors(location)
    #     DEVICES[location]["currentState"] = {
    #         "state": state,
    #         "brightness": brightness,
    #         "color": color,
    #         "color_temp": color_temp
    #     }
    
    # save_devices(DEVICES)  # save that current state

    while get_game_state(team_abbreviation) == "pre":
        print(f"--------------------------------")

        now=datetime.now()
        print(f"{now.strftime('%I:%M:%S %p')}\nWaiting for {team_abbreviation} game to start...")

        print(f"Next game for {team_abbreviation} is at {get_game_state(team_abbreviation)}")

        time.sleep(15)  # Wait for 15 seconds before checking again

    #run indefinitely to monitor the score, need to change till while game in progress
    while get_game_state(team_abbreviation) == "in":
        now=datetime.now()
        new_score = get_team_score(team_abbreviation)

        print(f"--------------------------------")
        print(f"{now.strftime('%I:%M:%S %p')}  {team_abbreviation} Score: {new_score}")

        if old_score != new_score:

            print(f"{team_abbreviation}: Score changed from {old_score} to {new_score}")
            score_trigger(team_abbreviation)  # Call the score_trigger function with the team abbreviation if there's a change
        # else:



            
            # handling this inside score trigger
            # for location in DEVICES:
            #         state, brightness, color, color_temp = get_current_device_colors(location)
            #         DEVICES[location]["currentState"] = {
            #             "state": state,
            #             "brightness": brightness,
            #             "color": color,
            #             "color_temp": color_temp
            #         }

            # save_devices(DEVICES)  # Save the updated DEVICES dictionary to the JSON file

        old_score = new_score

        next_call += 5
        sleep_time = next_call - time.monotonic()
        if sleep_time > 0:
            time.sleep(sleep_time)

    if get_game_state(team_abbreviation) == "post":
        game_summary = get_game_summary(team_abbreviation)

        team, my_score, my_hits, my_errors, my_records, opponent, opponent_score, opponent_hits, opponent_errors, opponent_records = get_game_summary(team_abbreviation)

        print(f"Final    Runs    Hits    Errors")
        print(f"{team}      {my_score}       {my_hits}       {my_errors}         ({my_records})")
        print(f"{opponent}      {opponent_score}       {opponent_hits}       {opponent_errors}         ({opponent_records})")

        print("-----------------------------------------------")
        matchup, date, shortDetail = get_next_game_start(team_abbreviation)
        print(f"Next game for {team_abbreviation}")
        print(matchup, shortDetail)


        print(date)

        cron_minute = date.minute
        cron_hour = date.hour
        cron_day = date.day
        cron_month = date.month

        print(cron_month, cron_day, cron_hour, cron_minute)
        time.sleep(15)  # Wait for 15 seconds before checking again

monitor_team = "CHC"  # Example team abbreviation

def run_monitor_team_score(team_abbreviation):
    while True:
        monitor_team_score(team_abbreviation, score_trigger)

# run_monitor_team_score()

if __name__ == "__main__":
    args = parse_args()
    monitor_team = get_selected_team(args)
    run_monitor_team_score(monitor_team)