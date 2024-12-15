import json

with open('settings.json', 'r') as stg:
    data = json.load(stg)

bot_token = data["token"]
