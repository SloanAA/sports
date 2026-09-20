import os
import json

DEVICES_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "govee_devices", "devices.json")
)


def load_devices():
    with open(DEVICES_PATH) as f:
        return json.load(f)


def save_devices(devices):
    with open(DEVICES_PATH, "w") as f:
        json.dump(devices, f, indent=2)
