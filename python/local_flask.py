from flask import Flask
from flask import request
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import string
import requests
import random
import httpx
import re

app = Flask(__name__)

def scrape_website(query, website_name, base_url, manhwa_page_url_selector, title_selector, cover_url_selector, chapter_number_selector):
    result = request_website_data(query, website_name, base_url, manhwa_page_url_selector, title_selector, cover_url_selector, chapter_number_selector)
    return result

@app.route('/asura', methods=['GET'])
def asura():
    query = request.args.get('query')
    result = request_website_data(query,
                            website_name="Asura",
                            base_url="https://asurascans.com/?s=",
                            manhwa_page_url_selector="div.bsx > a",
                            title_selector="div.bigor > div.tt",
                            cover_url_selector="div.limit > img",
                            chapter_number_selector="div.epxs",
                           )
    return result
   
@app.route('/luminous', methods=['GET'])
def luminous():
    query = request.args.get('query')
    result = request_website_data(query,
                            website_name="Luminous",
                            base_url="https://luminousscans.com/?s=",
                            manhwa_page_url_selector="div.bsx > a",
                            title_selector="div.bigor > div.tt",
                            cover_url_selector="div.limit > img",
                            chapter_number_selector="div.epxs",
                           )
    return result

@app.route('/flame', methods=['GET'])
def flame():
    query = request.args.get('query')
    result = request_website_data(query,
                            website_name="Flame",
                            base_url="https://flamescans.org/?s=",
                            manhwa_page_url_selector="div.bsx > a",
                            title_selector="div.bigor > div.tt",
                            cover_url_selector="div.limit > img",
                            chapter_number_selector="div.epxs",
                           )
    return result

@app.route('/reaper', methods=['GET'])
def reaper():
    query = request.args.get('query')
    result = reaper_scraper(1, query)
    return result

def request_website_data(query, website_name, base_url, manhwa_page_url_selector, title_selector, cover_url_selector, chapter_number_selector):
    try:
        formatted_url = base_url + query
        resp = requests.get(
            formatted_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
            },
        )
        resp.raise_for_status()

        manhwa_data = parse_data(
            resp,
            manhwa_page_url_selector,
            title_selector,
            cover_url_selector,
            chapter_number_selector,
        )

        return {
            "website": website_name,
            "manhwa_data": manhwa_data
        }
    except httpx.RequestError as e:
        raise Exception(f"Request error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def parse_data(resp, manhwa_page_url_selector, title_selector, cover_url_selector, chapter_number_selector):
    html = HTMLParser(resp.text)
    page_url = [
        element.attributes.get('href', '').strip()
        for element in html.css(manhwa_page_url_selector)
    ]

    title_elements = html.css(title_selector)
    titles = [title.text().strip() for title in title_elements]

    items = html.css(chapter_number_selector)
    chapters = [item.text().strip() for item in items]

    cover_url = [
        element.attributes.get('src', '').strip()
        for element in html.css(cover_url_selector)
    ]

    manhwa_data = []

    for i, title in enumerate(titles):
        data = {
            "title": title,
            "page_url": page_url[i],
            "cover_url": cover_url[i],
        }

        if chapters and i < len(chapters):
            numbers = re.findall(r'\d+', chapters[i])
            data["chapters"] = numbers[0] if numbers else ''


        manhwa_data.append(data)


    return manhwa_data



def reaper_scraper(page, query):
    base_url = "https://reaperscans.com"
    route_name = 'frontend.dtddzhx-ghvjlgrpt'
    
    response = requests.get(base_url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    },)

    soup = BeautifulSoup(response.content, 'html.parser')

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


    return {
            "website": "Reaper",
            "manhwa_data": manhwa_data,
           }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
