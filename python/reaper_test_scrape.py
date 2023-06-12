import random
import requests
import json
from bs4 import BeautifulSoup

def search_manga_request(page, query):
    base_url = "https://reaperscans.com/"
    route_name = 'frontend.dtddzhx-ghvjlgrpt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    csrf_token = soup.select_one("meta[name=\"csrf-token\"]")['content']

    livewire_data = soup.find(attrs={'wire:id': True})
    wire_id_value = livewire_data['wire:id']
    print(wire_id_value)

    #  Javascript: (Math.random() + 1).toString(36).substring(8)
    generate_id = lambda: "1." + str(random.randint(0, 36**5))[1:]  # Not exactly the same, but results in a 3-5 character string
    payload = {
        "fingerprint": wire_id_value,
        "serverMemo": None,
        "updates": [
            {
                "type": "syncInput",
                "payload": {
                    "id": generate_id(),
                    "name": "query",
                    "value": query
                }
            }
        ]
    }
    payload = json.dumps(payload)

    headers = {
        "x-csrf-token": csrf_token,
        "x-livewire": "true"
    }

    url = f"{base_url}/livewire/message/{route_name}"
    return requests.post(url, headers=headers, data=payload)


print(search_manga_request(1, '4000'))