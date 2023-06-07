import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from flask import Flask, jsonify
from selectolax.parser import HTMLParser
from datetime import datetime
from urllib.parse import urlparse
import json
import httpx
import threading
import ssl
import os
from PIL import Image
from io import BytesIO

service_account_key = 'service-account-credentials.json'

cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'manhwa-helper.appspot.com'
})

project_id = firebase_admin.get_app().project_id
print(f"Connected to Firebase project: {project_id}")

app = Flask(__name__)


@app.route('/thread_scraper', methods=['GET'])
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

    for thread in threads:
        thread.join()

    json_data = json.dumps(results)

    with open('manhwa_data.txt', 'w') as file:
        file.write(json_data)

    return jsonify(results)


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

    resized_images = []

    for i, link in enumerate(cover_link):
        try:
            max_width = 300
            response = httpx.get(link)
            image = Image.open(BytesIO(response.content))

            width, height = image.size
            ratio = max_width / width
            new_size = (max_width, int(height * ratio))
            resized_image = image.resize(new_size)

            _, ext = os.path.splitext(link)

            # Salvar no firebase storage
            bucket = storage.bucket()
            blob = bucket.blob(f'resized_image_{i+1}{ext}')
            blob.upload_from_string(resized_image.tobytes(
            ), content_type=f'image/{ext[1:]}')

            # Busca link onde foi salvo
            download_url = blob.generate_signed_url(
                expiration=300, method='GET')

            # resized_images.append(link)
            resized_images.append(download_url)

            print(f"Image {i+1} resized and saved as {ext}")
        except Exception as e:
            resized_images.append(link)
            write_log(
                f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Server: Error while resizing image {link}")
            print(f"{str(e)}")

        # image_path = download_image(link)
        # resized_image_path = resize_image(image_path)
        # resized_images.append(resized_image_path)

    print(resized_images)

    manhwa_data = []
    for i, title in enumerate(titles):
        if i >= 10:
            break
        manhwa_data.append({
            "title": title,
            "cover_link": cover_link[i],
            "chapters": chapters[i * 3: (i + 1) * 3],
            "chapters_links": chapters_links[i * 3: (i + 1) * 3],
        })

    return manhwa_data


def download_image(url):
    response = httpx.get(url)
    response.raise_for_status()

    filename = os.path.basename(urlparse(url).path)

    image_path = os.path.join("images/", filename)
    with open(image_path, "wb") as file:
        file.write(response.content)

    return image_path


def resize_image(image_path):
    image = Image.open(image_path)

    max_width = 300
    width, height = image.size
    ratio = max_width / width
    new_width = max_width
    new_height = int(height * ratio)

    resized_image = image.resize((new_width, new_height))

    resized_image_path = os.path.splitext(image_path)[0] + "_resized.png"
    resized_image.save(resized_image_path, format="PNG")

    return resized_image_path


def write_log(log_message):
    with open('scraping_logs.txt', 'a') as file:
        file.write(log_message + '\n')


if __name__ == "__main__":
    app.run()
