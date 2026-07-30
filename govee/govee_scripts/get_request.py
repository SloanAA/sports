import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()  # finds and reads .env in the current directory

url = "https://openapi.api.govee.com/router/api/v1/user/devices"

headers = {
    "Content-Type": "application/json",
    "Govee-API-Key": os.getenv("GOVEE_KEY")
}

response = requests.get(url, headers=headers)  # no need for data={}, GET has no body

if response.status_code != 200:
    print(f"Error {response.status_code}: {response.text}")
else:
    data = response.json()
    print(json.dumps(data, indent=2))