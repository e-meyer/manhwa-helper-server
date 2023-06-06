from flask import Flask, jsonify
from selectolax.parser import HTMLParser
from datetime import datetime
import json
import httpx
import threading
import ssl

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


def parse_data(resp, title_selector, chapters_selector, chapterslink_selector, coverlink_selector):
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


def write_log(log_message):
    with open('scraping_logs.txt', 'a') as file:
        file.write(log_message + '\n')


if __name__ == "__main__":
    app.run()
