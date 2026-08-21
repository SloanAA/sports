from test_scripts.next_game import get_next_game
from test_scripts.team_specific_score import get_team_score
import time
import threading
from govee.govee_scripts.load_and_save import load_devices, save_devices
from govee.govee_scripts.put_request import rgbLight, colorTempLight
from team_color import get_team_color
from govee.govee_scripts.state_request import get_current_device_colors, DEVICES
from concurrent.futures import ThreadPoolExecutor
from test_scripts.game_live import get_game_state
from datetime import datetime
from score_trigger import score_trigger
from test_scripts.game_summary import get_game_summary
import json
import os



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
        print(f"{now.strftime("%I:%M:%S %p")}\nWaiting for {team_abbreviation} game to start...")

        print(f"Next game for {team_abbreviation} is at {get_next_game(team_abbreviation)}")

        time.sleep(15)  # Wait for 15 seconds before checking again

    #run indefinitely to monitor the score, need to change till while game in progress
    while get_game_state(team_abbreviation) == "in":
        now=datetime.now()
        new_score = get_team_score(team_abbreviation)

        print(f"--------------------------------")
        print(f"{now.strftime("%I:%M:%S %p")}  {team_abbreviation} Score: {new_score}")

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


monitor_team = "CHC"  # Example team abbreviation
monitor_team_score(monitor_team, score_trigger)