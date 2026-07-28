import os
import requests
from dotenv import load_dotenv


load_dotenv()  # finds and reads .env in the current directory

url = "http://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"

payload={}
# headers = {
#   'x-apisports-key': os.environ['API_SPORTS_KEY']
# }

response = requests.request("GET", url, data=payload)

print(response.text)