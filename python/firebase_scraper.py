import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from flask import Flask, jsonify
from selectolax.parser import HTMLParser
from datetime import datetime
import json
import httpx
import threading
import ssl
import os
from PIL import Image
from io import BytesIO

from notifications import send_notification_topic

service_account_key = 'service-account-credentials.json'

cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'manhwa-helper.appspot.com'
})

project_id = firebase_admin.get_app().project_id
print(f"Connected to Firebase project: {project_id}")

# app = Flask(__name__)


# @app.route('/thread_scraper', methods=['GET'])
def scrape_data():
    threads = []

    def scrape_website(website, url, title_selector, chapters_selector, chapterlinks_selector, coverlink_selector):
        try:
            result = get_data(website, url, title_selector,
                              chapters_selector, chapterlinks_selector, coverlink_selector)
            results.append(result)
            write_log(
                f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Server: Success scraping {website}")
        except Exception as e:
            write_log(
                f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Server: Error while scraping {website}")
            write_log(str(e))

    results = []

    t1 = threading.Thread(
        target=scrape_website,
        args=("Asura",
              "https://www.asurascans.com/",
              "div.luf > a.series",
              "div.luf > ul > li > a",
              "div.luf > ul > li > a",
              "div.imgu > a.series > img"
              ),
    )
    threads.append(t1)
    t1.start()

    t2 = threading.Thread(
        target=scrape_website,
        args=("Flame",
              "https://flamescans.org/",
              "div.bigor > div.info > a",
              "div.adds > div.epxs",
              "div.chapter-list > a",
              "div.latest-updates > div.bs > div.bsx > a > div.limit > img"
              ),
    )
    threads.append(t2)
    t2.start()

    t3 = threading.Thread(
        target=scrape_website,
        args=("Luminous",
              "https://luminousscans.com/",
              "div.luf > a.series",
              "div.luf > ul > li > a",
              "div.luf > ul > li > a",
              "div.imgu > a.series > img"
              ),
    )
    threads.append(t3)
    t3.start()

    for thread in threads:
        thread.join()

    json_data = json.dumps(results)
    json_object = json.loads(json_data)

    with open('manhwa_data.txt', 'r') as file:
        existing_data = json.load(file)

    websites = set()
    for item in existing_data:
        website = item['website']
        websites.add(website)

    existing_titles = {}
    for item in existing_data:
        website = item['website']
        existing_titles[website] = set()
        for manhwa in item['manhwa_data']:
            existing_titles[website].add(manhwa['title'])

    new_titles = {}
    for item in json_object:
        website = item['website']
        new_titles[website] = set()
        for manhwa in item['manhwa_data']:
            new_titles[website].add(manhwa['title'])

    # print(existing_titles)
    # print(new_titles)

    new_and_unique_titles = []
    for website in existing_titles.keys():
        new_titles_for_website = list(new_titles.get(
            website, set()) - existing_titles[website])
        new_and_unique_titles.extend(new_titles_for_website)

    print(new_and_unique_titles)

    for manhwa in new_and_unique_titles:
        clean_title = "_".join(manhwa.strip().lower().replace('`', '').replace('’', '').replace(',', '').replace('\'', '').split(" "))
        print(clean_title)
        send_notification_topic(clean_title)

    with open('manhwa_data.txt', 'w') as file:
        file.write(json_data)

    return json.dumps(results)


def get_data(website, url, title_selector, chapters_selector, chapterlinks_selector, coverlink_selector):
    try:
        resp = httpx.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
            },
            verify=ssl.CERT_NONE
        )
        resp.raise_for_status()

        manhwa_data = parse_data(
            resp,
            website,
            title_selector,
            chapters_selector,
            chapterlinks_selector,
            coverlink_selector
        )

        return {
            "website": website,
            "manhwa_data": manhwa_data[:10]
        }
    except httpx.RequestError as e:
        raise Exception(f"Request error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def parse_data(resp, website, title_selector, chapters_selector, chapterslink_selector, coverlink_selector):
    html = HTMLParser(resp.text)
    titles = [
        element.attributes.get('title', '').strip()
        for element in html.css(title_selector)
    ]

    items = html.css(chapters_selector)
    chapters = [item.text().strip() for item in items]

    chapters_links = [
        element.attributes.get('href', '').strip()
        for element in html.css(chapterslink_selector)
        if "title" not in element.attributes
    ]

    cover_link = [
        element.attributes.get('src', '').strip()
        for element in html.css(coverlink_selector)
    ]

    # resized_images = []

    # for i, link in enumerate(cover_link):
    #     try:
    #         max_width = 300
    #         response = httpx.get(link)
    #         image = Image.open(BytesIO(response.content))

    #         width, height = image.size
    #         ratio = max_width / width
    #         new_size = (max_width, int(height * ratio))
    #         resized_image = image.resize(new_size)

    #         _, ext = os.path.splitext(link)

    #         # Salvar no firebase storage
    #         bucket = storage.bucket()
    #         blob = bucket.blob(f'resized_image_{i+1}{ext}')
    #         blob.upload_from_string(resized_image.tobytes(
    #         ), content_type=f'image/{ext[1:]}')

    #         # Busca link onde foi salvo
    #         download_url = blob.generate_signed_url(
    #             expiration=300, method='GET')

    #         # resized_images.append(link)
    #         resized_images.append(download_url)

    #         print(f"Image {i+1} resized and saved as {ext}")
    #     except Exception as e:
    #         resized_images.append(link)
    #         write_log(
    #             f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Server: Error while resizing image {link}")
    #         print(f"{str(e)}")

    # print(resized_images)


    manhwa_data = []
    for i, title in enumerate(titles):
        # if title == 'The Player Hides His Past':
        #     title = 'wrong_name_wrong_name_wrong_name_wrong_name'
        # if title == 'Nine Heavens Swordmaster':
        #     title = 'wrong_name_wrong_name_wrong_name_wrong_name'
        if i >= 10:
            break
        manhwa_data.append({
            "title": title,
            "cover_link": cover_link[i],
            "chapters": chapters[i * 3: (i + 1) * 3],
            "chapters_links": chapters_links[i * 3: (i + 1) * 3],
        })

    return manhwa_data


def write_log(log_message):
    with open('scraping_logs.txt', 'a') as file:
        file.write(log_message + '\n')


if __name__ == "__main__":
    while True:
        try:
            scrape_data()
            time.sleep(300)  # Sleep for 300 seconds (5 minutes)
        except KeyboardInterrupt:
            print("Stopping the scraper")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(300)  # Sleep for 5 minutes before trying again
