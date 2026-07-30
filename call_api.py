from test_scripts.team_specific_score import get_team_score
import time
import threading

def monitor_team_score(team_abbreviation):
    next_call = time.monotonic()
    old_score = 0

    while True:
        new_score = get_team_score(team_abbreviation)
        print(f"{team_abbreviation} Score: {new_score}")
        if old_score != new_score:
            print(f"{team_abbreviation}: Score changed from {old_score} to {new_score}")
        old_score = new_score

        next_call += 5
        sleep_time = next_call - time.monotonic()
        if sleep_time > 0:
            time.sleep(sleep_time)


monitor_team = 'CHC'  # Example team abbreviation
monitor_team_score(monitor_team)