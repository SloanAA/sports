import requests
import os
from dotenv import load_dotenv
import json
from load_and_save import load_devices, save_devices

load_dotenv()  # finds and reads .env in the current directory

url = "https://openapi.api.govee.com/router/api/v1/device/state"  # Corrected URL for the Govee API state endpoint

headers = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_KEY")
}


DEVICES = load_devices()  # Load devices from the JSON file


def get_current_device_colors(light_location):
    light_info = DEVICES[light_location]  # Get the device info for the specified location

    payload = {
        "requestId": light_info["device"] + "_state_request",
        "payload": {
            "sku": light_info["sku"],
            "device": light_info["device"]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None, None, None, None  # Return None values if there's an error
    
    data = response.json()

    values_by_instance = {
        cap["instance"]: cap["state"]["value"]
        for cap in data["payload"]["capabilities"]
    }

    state = values_by_instance.get("powerSwitch")
    brightness = values_by_instance.get("brightness")
    color_temp = values_by_instance.get("colorTemperatureK")

    color = values_by_instance.get("colorRgb")
    if color_temp != None:
        color = f"{color:06x}"

    print(f"{light_location}: state={'On' if state else 'Off'}, "
          f"brightness={brightness}, color=#{color}, color_temp={color_temp}K")

    return state, brightness, color, color_temp

get_current_device_colors("office2")  # Example usage for the "office1" device