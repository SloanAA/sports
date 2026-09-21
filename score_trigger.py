import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baseball.mlb.espn.game.espn_game_start import get_game_start
from baseball.mlb.espn.team.mlb_team_score import get_team_score
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import threading
from govee.govee_scripts.govee_load_and_save import load_devices, save_devices
from govee.govee_scripts.govee_put import onOffLight, rgbBrightness, rgbLight, colorTempLight
from baseball.mlb.team.mlb_team_color import get_team_color
from govee.govee_scripts.govee_state import get_current_device_colors, DEVICES, update_device_state
from concurrent.futures import ThreadPoolExecutor
from baseball.mlb.espn.game.espn_game_status import get_game_state
from datetime import datetime
import json
import os
from govee.govee_scripts.govee_config import get_brightness_setting

#should really make a scene because this govee api call is SLOW 

def score_trigger(team_abbreviation): #still triggers on None --> 0
    print("Score changed! Triggering Govee lights.")


    #this should look at all the states really easily and should be threaded
    with ThreadPoolExecutor(max_workers=len(DEVICES)) as executor:
        for location in DEVICES:
            executor.submit(update_device_state, location)


    colors = list(get_team_color(team_abbreviation))

    for n in range(4):  # Change the lights 4 times
        with ThreadPoolExecutor(max_workers=len(DEVICES)) as executor:
            for i, location in enumerate(DEVICES):
                color = colors[(i + n) % len(colors)]  # Cycle through the colors
                executor.submit(rgbLight, location, color)
        print("CHANGE LIGHTS")
        print(f"{n} fetch at {datetime.now(ZoneInfo("America/New_York"))}")
        time.sleep(1)

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

team_abbreviation = "CHC"
score_trigger(team_abbreviation)