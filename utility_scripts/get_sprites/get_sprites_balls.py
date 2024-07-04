import requests
import os

base_url = 'https://pokeapi.co/api/v2/item/'

apriballs = ['fast-ball',
 'lure-ball',
 'level-ball',
 'heavy-ball',
 'love-ball',
 'moon-ball',
 'dream-ball',
 'safari-ball',
 'beast-ball',
 'sport-ball']

for ball in apriballs:
    response = requests.get(base_url + ball)

    if response.status_code == 200:
        data = response.json()
        sprite_url = data['sprites']['default']

        with open('static/sprites/'+ball+'.png', 'wb') as file:
            asset_response = requests.get(sprite_url)
            if asset_response.status_code == 200:
                file.write(asset_response.content)
            else:
                print(f"Failed to download asset for '{ball}': {asset_response.status_code}")
    else:
        print(f"Request failed for item '{ball}': {response.status_code}")