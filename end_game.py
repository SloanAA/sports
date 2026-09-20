#this function is a rewritten score trigger

#win = true  - green
#loss = false  - red
import govee


import threading
from concurrent.futures import ThreadPoolExecutor

import time
from datetime import datetime
import json
import os
# from govee.govee_scripts.govee_settings import get_brightness_setting

def end_game_trigger(outcome): #still triggers on None --> 0
    print("Score changed! Triggering Govee lights.")


    #this should look at all the states really easily and should be threaded
    with ThreadPoolExecutor(max_workers=len(govee.DEVICES)) as executor:
        for location in govee.DEVICES:
            executor.submit(govee.update_device_state, location)



    with ThreadPoolExecutor(max_workers=len(govee.DEVICES)) as executor:
        for location in govee.DEVICES:
            executor.submit(govee.rgbLight, location, "#00FF00" if outcome else "#FF0000")

    time.sleep(5)  # Change the lights to outcome for 5 seconds
    print("CHANGE LIGHTS")

    with ThreadPoolExecutor(max_workers=len(govee.DEVICES) * 2) as executor:
        print("Restoring previous state of lights...")
        for location in govee.DEVICES:
            previous = govee.DEVICES[location]["previousState"]

            # where we actually restore current state
            state = previous["state"]

            color = previous["color"]
            color_temp = previous["color_temp"]
            brightness = previous["brightness"]

            # print(f"{location}, {state}, {color}, {color_temp}, {brightness}")
            if (state == 0):
                executor.submit(govee.onOffLight, location, 0)
            else:
                if color_temp:
                    executor.submit(govee.colorTempLight, location, color_temp)
                    # print(f"{location}: restoring {color_temp}K")
                else:
                    executor.submit(govee.rgbLight, location, color)
                    # print(f"{location}: restoring {color}")

                executor.submit(govee.rgbBrightness, location, brightness)
                # print(f"{location}: restoring brightness {brightness}")

        print("Done score trigger")

end_game_trigger(True)  # Call the end_game_trigger function with True for a win
#stop