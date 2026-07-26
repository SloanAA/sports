import os
import requests
from dotenv import load_dotenv


load_dotenv()  # finds and reads .env in the current directory

url = "https://v1.baseball.api-sports.io/leagues"

payload={}
headers = {
  'x-apisports-key': os.environ['API_SPORTS_KEY']
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)