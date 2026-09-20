import os
import json


DEVICES_PATH = os.path.join(os.path.dirname(__file__), "devices.json") #this is how we write to the new devices.json file, which is in the same directory as this script

def load_devices():
    with open(DEVICES_PATH) as f:
        return json.load(f)


def save_devices(devices):
    with open(DEVICES_PATH, "w") as f:
        json.dump(devices, f, indent=2)
