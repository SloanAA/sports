import requests
import os
from dotenv import load_dotenv
import json
from devices import DEVICES

load_dotenv()  # finds and reads .env in the current directory

url = "https://openapi.api.govee.com/router/api/v1/device/control"  # Corrected URL for the Govee API control endpoint

headers = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_KEY")
}

def onOffLight(light_location,light_state):
    light_info = DEVICES[light_location]  # Get the device info for the specified location

    payload = {
        "requestId": "officeLight1_on",
        "payload": {
            "sku": light_info["sku"],
            "device": light_info["device"],
            "capability": {
                "type": "devices.capabilities.on_off",
                "instance": "powerSwitch",
                "value": light_state
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
    else:
        data = response.json()
        print(json.dumps(data, indent=2))




def rgbLight(light_location,hex_color):
    light_info = DEVICES[light_location]  # Get the device info for the specified location
    decimal_value = int(hex_color.lstrip("#"), 16)

    payload = {
        "requestId": "officeLight1_on",
        "payload": {
            "sku": light_info["sku"],
            "device": light_info["device"],
            "capability": {
                # "type": "devices.capabilities.on_off",
                # "instance": "powerSwitch",
                # "value": 0
                "type": "devices.capabilities.color_setting",
                "instance": "colorRgb",
                "value": decimal_value
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
    else:
        data = response.json()
        print(json.dumps(data, indent=2))


onOffLight("office1", 1)  # Turn on the light
rgbLight("office1", "#FF0000")