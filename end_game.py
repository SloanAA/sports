#this function is a rewritten score trigger

#win = true  - green
#loss = false  - red
from test_scripts.game_start import get_game_start
from test_scripts.team_specific_score import get_team_score
import time
import threading
from govee.govee_scripts.load_and_save import load_devices, save_devices
from govee.govee_scripts.put_request import onOffLight, rgbBrightness, rgbLight, colorTempLight
from team_color import get_team_color
from govee.govee_scripts.state_request import get_current_device_colors, DEVICES, update_device_state
from concurrent.futures import ThreadPoolExecutor
from test_scripts.game_live import get_game_state
from datetime import datetime
import json
import os
from govee.govee_scripts.brightnessSetting import get_brightness_setting

def end_game_trigger(outcome): #still triggers on None --> 0
    print("Score changed! Triggering Govee lights.")


    #this should look at all the states really easily and should be threaded
    with ThreadPoolExecutor(max_workers=len(DEVICES)) as executor:
        for location in DEVICES:
            executor.submit(update_device_state, location)



    with ThreadPoolExecutor(max_workers=len(DEVICES)) as executor:
        for location in DEVICES:
            executor.submit(rgbLight, location, "#00FF00" if outcome else "#FF0000")

    time.sleep(5)  # Change the lights to outcome for 5 seconds
    print("CHANGE LIGHTS")

    with ThreadPoolExecutor(max_workers=len(DEVICES) * 2) as executor:
        print("Restoring previous state of lights...")
        for location in DEVICES:
            previous = DEVICES[location]["previousState"]

            # where we actually restore current state
            state = previous["state"]

            color = previous["color"]
            color_temp = previous["color_temp"]
            brightness = previous["brightness"]

            # print(f"{location}, {state}, {color}, {color_temp}, {brightness}")
            if (state == 0):
                executor.submit(onOffLight, location, 0)
            else:
                if color_temp:
                    executor.submit(colorTempLight, location, color_temp)
                    # print(f"{location}: restoring {color_temp}K")
                else:
                    executor.submit(rgbLight, location, color)
                    # print(f"{location}: restoring {color}")

                executor.submit(rgbBrightness, location, brightness)
                # print(f"{location}: restoring brightness {brightness}")

        print("Done score trigger")

# end_game_trigger(True)  # Call the end_game_trigger function with True for a win
#stop