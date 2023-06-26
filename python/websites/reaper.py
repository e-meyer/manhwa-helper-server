from bs4 import BeautifulSoup
import string
import random
import json
import re
import requests

def reaper_search_scraper(result, query):
    soup = BeautifulSoup(result.text, 'html.parser')

    csrf_token = soup.select_one("meta[name=\"csrf-token\"]")['content']

    livewire_data = soup.find(attrs={'wire:initial-data': True})
    wire_sv_memo = livewire_data['wire:initial-data']
    json_data = json.loads(wire_sv_memo)

    def generate_random_string():
        characters = string.digits + string.ascii_lowercase
        random_length = random.randint(4, 5)
        random_string = ''.join(random.choices(characters, k=random_length))
        return random_string

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

    req = requests.post(
        url='https://reaperscans.com/livewire/message/frontend.dtddzhx-ghvjlgrpt', headers=headers, data=payload)

    json_data = json.loads(req.content)
    html_content = json_data["effects"]["html"]

    content = BeautifulSoup(html_content, "html.parser")

    manhwa_list = content.find_all('li', attrs={'wire:key': lambda value: value and 'search-comic' in value})

    manhwa_data = []

    for manhwa in manhwa_list:
        # a_tag 
        a_tag = manhwa.find('a')
        
        # Title and number of chapters
        p_tags = a_tag.find_all('p')
        manhwa_title = p_tags[0].text.strip()
        chapters_number = p_tags[1].find_all('span')[-1].text.strip()

        numbers = re.findall(r'\d+', chapters_number)

        # Cover url
        img_tag = a_tag.find('div').find('img')
        cover_url = img_tag['src']
        
        # Manhwa details apge
        manhwa_page_url = a_tag['href']

        

        manhwa_data.append({
            "title": manhwa_title,
            "page_url": manhwa_page_url,
            "cover_url": cover_url,
            "chapters": numbers[0] if numbers else '',
        })


    return manhwa_data