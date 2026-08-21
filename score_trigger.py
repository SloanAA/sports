from test_scripts.next_game import get_next_game
from test_scripts.team_specific_score import get_team_score
import time
import threading
from govee.govee_scripts.load_and_save import load_devices, save_devices
from govee.govee_scripts.put_request import onOffLight, rgbBrightness, rgbLight, colorTempLight
from team_color import get_team_color
from govee.govee_scripts.state_request import get_current_device_colors, DEVICES
from concurrent.futures import ThreadPoolExecutor
from test_scripts.game_live import get_game_state
from datetime import datetime
import json
import os
from brightnessSetting import get_brightness_setting


def score_trigger(team_abbreviation): #still triggers on None --> 0
    print("Score changed! Triggering Govee lights.")


    for location in DEVICES:
        state, brightness, color, color_temp = get_current_device_colors(location)
        DEVICES[location]["currentState"] = {
            "state": state,
            "brightness": brightness,
            "color": color,
            "color_temp": color_temp
        }
        #  print(f"Current State: {DEVICES[location]["currentState"]}")
        DEVICES[location]["previousState"] = DEVICES[location]["currentState"]  # Save the current state as previous state
        score_trigger_brightness = get_brightness_setting()
        rgbBrightness(location, score_trigger_brightness)


    colors = list(get_team_color(team_abbreviation))

    for n in range(4):  # Change the lights 4 times
        with ThreadPoolExecutor(max_workers=len(DEVICES)) as executor:
            for i, location in enumerate(DEVICES):
                color = colors[(i + n) % len(colors)]  # Cycle through the colors
                executor.submit(rgbLight, location, color)
            time.sleep(1)
            print("WAIT")

    with ThreadPoolExecutor(max_workers=len(DEVICES) * 2) as executor:
        print("Restoring previous state of lights...")
        for location in DEVICES:
            previous = DEVICES[location]["previousState"]

            # where we actually restore current state
            state = previous["state"]

            color = previous["color"]
            color_temp = previous["color_temp"]
            brightness = previous["brightness"]

            print(f"{location}, {state}, {color}, {color_temp}, {brightness}")
            if (state == 0):
                executor.submit(onOffLight, location, 0)
            else:
                if color_temp:
                    executor.submit(colorTempLight, location, color_temp)
                    print(f"{location}: restoring {color_temp}K")
                else:
                    executor.submit(rgbLight, location, color)
                    print(f"{location}: restoring {color}")

                executor.submit(rgbBrightness, location, brightness)
                print(f"{location}: restoring brightness {brightness}")

        print("Done score trigger")

# team_abbreviation = "CHC"
# score_trigger(team_abbreviation)