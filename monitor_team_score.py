from test_scripts.team_specific_score import get_team_score
import time
import threading
from govee.govee_scripts.load_and_save import load_devices, save_devices
from govee.govee_scripts.put_request import rgbLight, colorTempLight
from team_color import get_team_color
from govee.govee_scripts.state_request import get_current_device_colors, DEVICES
from concurrent.futures import ThreadPoolExecutor
import json
import os



def monitor_team_score(team_abbreviation, score_trigger):
    next_call = time.monotonic()
    old_score = 0

    #establish a current state when first running script
    for location in DEVICES:
        state, brightness, color, color_temp = get_current_device_colors(location)
        DEVICES[location]["currentState"] = {
            "state": state,
            "brightness": brightness,
            "color": color,
            "color_temp": color_temp
        }
    
    save_devices(DEVICES)  # save that current state

    #run indefinitely to monitor the score, need to change till while game in progress
    while True:

        new_score = get_team_score(team_abbreviation)
        print(f"--------------------------------")
        print(f"{team_abbreviation} Score: {new_score}")

        if old_score != new_score:

            print(f"{team_abbreviation}: Score changed from {old_score} to {new_score}")
            score_trigger(team_abbreviation)  # Call the score_trigger function with the team abbreviation if there's a change
        else:

            

            for location in DEVICES:
                    state, brightness, color, color_temp = get_current_device_colors(location)
                    DEVICES[location]["currentState"] = {
                        "state": state,
                        "brightness": brightness,
                        "color": color,
                        "color_temp": color_temp
                    }

            save_devices(DEVICES)  # Save the updated DEVICES dictionary to the JSON file

        old_score = new_score

        next_call += 5
        sleep_time = next_call - time.monotonic()
        if sleep_time > 0:
            time.sleep(sleep_time)

def score_trigger(team_abbreviation): #still triggers on None --> 0
    print("Score changed! Triggering Govee lights.")

    for location in DEVICES:
         DEVICES[location]["previousState"] = DEVICES[location]["currentState"]  # Save the current state as previous state


    colors = list(get_team_color(team_abbreviation))

    for n in range(4):  # Change the lights 4 times
        with ThreadPoolExecutor(max_workers=len(DEVICES)) as executor:
            for i, location in enumerate(DEVICES):
                color = colors[(i + n) % len(colors)]  # Cycle through the colors
                executor.submit(rgbLight, location, color)
            time.sleep(1)
            print("WAIT")

    with ThreadPoolExecutor(max_workers=len(DEVICES) * 2) as executor:
        for location in DEVICES:
            previous = DEVICES[location]["previousState"]

            color = previous["color"]
            color_temp = previous["color_temp"]

            if color_temp:
                executor.submit(colorTempLight, location, color_temp)
                print(f"{location}: restoring {color_temp}K")
            else:
                executor.submit(rgbLight, location, color)
                print(f"{location}: restoring {color}")

        print("Done score trigger")

monitor_team = "SEA"  # Example team abbreviation
monitor_team_score(monitor_team, score_trigger)