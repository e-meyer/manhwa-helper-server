import random
import requests
import json
from bs4 import BeautifulSoup
import random
import string


def search_manga_request(page, query):
    base_url = "https://reaperscans.com"
    route_name = 'frontend.dtddzhx-ghvjlgrpt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    csrf_token = soup.select_one("meta[name=\"csrf-token\"]")['content']
    print(csrf_token)

    livewire_data = soup.find(attrs={'wire:initial-data': True})
    wire_id_value = livewire_data['wire:id']
    wire_sv_memo = livewire_data['wire:initial-data']
    json_data = json.loads(wire_sv_memo)
    # print(json_data['fingerprint'])
    # print(json_data['serverMemo'])

    def generate_random_string():
        characters = string.digits + string.ascii_lowercase
        random_length = random.randint(4, 5)
        random_string = ''.join(random.choices(characters, k=random_length))
        return random_string
    print(generate_random_string())
    # #  Javascript: (Math.random() + 1).toString(36).substring(8)
    payload = {
        "fingerprint": json_data['fingerprint'],
        "serverMemo": json_data['serverMemo'],
        "updates": [
            {
                "type": "syncInput",
                "payload": {
                    "id": generate_random_string(),
                    "name": "query",
                    "value": query
                }
            }
        ]
    }
    payload = json.dumps(payload)

    headers = {
        "content-type": "application/json",
        "Accept": "text/html, application/xhtml+xml",
        "Origin": "https://reaperscans.com",
        "Refeer": "https://reaperscans.com",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "X-Csrf-Token": csrf_token,
        "X-Livewire": "true",
    }

    url = f"{base_url}/livewire/message/{route_name}"

    print(url)
    print('headers')
    print(headers)
    print('payload')
    print(payload)
    print('fingerprint')
    print(json_data['fingerprint'])
    print('serverMemo')
    print(json_data['serverMemo'])

    req = requests.post(
        url='https://reaperscans.com/livewire/message/frontend.dtddzhx-ghvjlgrpt', headers=headers, data=payload)
    print(response.status_code)
    return req.content


print(search_manga_request(1, 'Estio'))


# json_str = '{"fingerprint":{"id":"9FsA8fzaaMH3zxn9Cobo","name":"frontend.dtddzhx-ghvjlgrpt","locale":"en","path":"\/","method":"GET","v":"acj"},"effects":{"listeners":[]},"serverMemo":{"children":[],"errors":[],"htmlHash":"45b5366f","data":{"query":"","comics":[],"novels":[]},"dataMeta":[],"checksum":"c2e880587be2b53795003dd12315b17fc9eb7e8bfff561c83b2b89511ee4d444"}}'
# print(json_str)
