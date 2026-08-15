import requests
import os
from dotenv import load_dotenv
import json
from load_and_save import load_devices, save_devices

load_dotenv()  # finds and reads .env in the current directory

url = "https://openapi.api.govee.com/router/api/v1/device/control"  # Corrected URL for the Govee API control endpoint

headers = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_KEY")
}


DEVICES = load_devices()  # Load devices from the JSON file



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
        DEVICES[light_location]["state"] = light_state  # Update the state in the DEVICES dictionary
        save_devices(DEVICES)  # Save the updated DEVICES dictionary to the JSON file
        print(json.dumps(data, indent=2))




def rgbLight(light_location, hex_color):
    light_info = DEVICES[light_location]
    decimal_value = int(hex_color.lstrip("#"), 16)

    payload = {
        "requestId": light_info["device"] + "_color_change",
        "payload": {
            "sku": light_info["sku"],
            "device": light_info["device"],
            "capability": {
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
        DEVICES[light_location]["color"] = hex_color  # Update the color in the DEVICES dictionary
        save_devices(DEVICES)  # Save the updated DEVICES dictionary to the JSON file
        print(light_location + " color changed to " + hex_color)
        


rgbLight("office2", "#00FF00")  # Change the light color to red
onOffLight("office2", 1)  # Turn on the light