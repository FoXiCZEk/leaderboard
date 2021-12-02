import requests
import json
data = requests.get("https://dayzsalauncher.com/#/servercheck/82.208.17.115:28582")
print(f"{data.text}")
