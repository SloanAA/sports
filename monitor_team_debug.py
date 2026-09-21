import baseball.mlb as mlb
import time
import threading
import govee
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from score_trigger import score_trigger
import json
import os

from end_game import end_game_trigger

import argparse

debug = False


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor a team's live score.")
    parser.add_argument("team", help="Team name or abbreviation, e.g. 'yankees' or 'nyy'")
    return parser.parse_args()


def get_selected_team(args):
    key = args.team.lower().replace(" ", "")
    if key not in mlb.team_abbreviations.TEAM_ABBREVIATIONS:
        valid = ", ".join(sorted(set(mlb.team_abbreviations.TEAM_ABBREVIATIONS.keys())))
        raise SystemExit(f"Unknown team '{args.team}'. Valid options:\n{valid}")
    return mlb.team_abbreviations.TEAM_ABBREVIATIONS[key]



def monitor_team_score(team_abbreviation, score_trigger):
    next_call = time.monotonic()
    old_score = 0


    while mlb.get_game_state(team_abbreviation) == "pre":
        print(f"--------------------------------")
        now=datetime.now()
        print(f"{now.strftime('%I:%M:%S %p')}\nWaiting for {team_abbreviation} game to start...")
        print(f"Next game for {team_abbreviation} is at {mlb.get_game_state(team_abbreviation)}")

        time.sleep(15)  # Wait for 15 seconds before checking again

    #run indefinitely to monitor the score, need to change till while game in progress
    if mlb.get_game_state(team_abbreviation) == "in":
        now=datetime.now()
        new_score = mlb.get_team_score(team_abbreviation)
        print(f"--------------------------------")
        print(f"{now.strftime('%I:%M:%S %p')}  {team_abbreviation} Score: {new_score}")

    while mlb.get_game_state(team_abbreviation) == "in":
        now=datetime.now()
        new_score = mlb.get_team_score(team_abbreviation)

        if old_score != new_score:

            print(f"{team_abbreviation}: Score changed from {old_score} to {new_score}")
            score_trigger(team_abbreviation)  # Call the score_trigger function with the team abbreviation if there's a change

        old_score = new_score

        next_call += 5
        sleep_time = next_call - time.monotonic()
        if sleep_time > 0:
            time.sleep(sleep_time)

    if mlb.get_game_state(team_abbreviation) == "post":
        game_summary = mlb.get_game_summary(team_abbreviation)

        team, my_score, my_hits, my_errors, my_records, opponent, opponent_score, opponent_hits, opponent_errors, opponent_records = mlb.get_game_summary(team_abbreviation)

        print(f"Final    Runs    Hits    Errors")
        print(f"{team}      {my_score}       {my_hits}       {my_errors}         ({my_records})")
        print(f"{opponent}      {opponent_score}       {opponent_hits}       {opponent_errors}         ({opponent_records})")

        print("-----------------------------------------------")
        matchup, date, shortDetail = mlb.get_next_game_start(team_abbreviation)
        print(f"Next game for {team_abbreviation}")
        print(matchup, shortDetail)

        score_trigger(team_abbreviation)  # Call the score_trigger function with the team abbreviation when the game is over
        #lets me know the game is over

        end_game_trigger(my_score > opponent_score)  # Call the end_game_trigger function with True for a win, False for a loss



        while mlb.get_game_state(team_abbreviation) == "post":
            time.sleep(60) #stays in this function and just waits here

monitor_team = "CHC"  # Example team abbreviation

def run_monitor_team_score(team_abbreviation):
    while True:
        monitor_team_score(team_abbreviation, score_trigger)

# run_monitor_team_score()

if __name__ == "__main__":
    args = parse_args()
    monitor_team = get_selected_team(args)
    run_monitor_team_score(monitor_team)