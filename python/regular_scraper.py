from flask import Flask, jsonify
import httpx
from selectolax.parser import HTMLParser

app = Flask(__name__)

@app.route('/regular_scraper', methods=['GET'])
def scrape_data():
    results = [
        get_data(
            "Asura",
            "https://www.asurascans.com/",
            "div.luf > a.series",
            "div.luf > ul > li > a"
        ),
        get_data(
            "Flame",
            "https://flamescans.org/",
            "div.bigor > div.info > a",
            "div.adds > div.epxs",
            "div.chapter-list > a"
        ),
        get_data(
            "Luminous",
            "https://luminousscans.com/",
            "div.luf > a.series",
            "div.luf > ul > li > a"
        ),
    ]
    return jsonify(results)

def get_data(website, url, title_selector, chapters_selector, chapterlinks_selector=None):
    resp = httpx.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )

    manhwa_data = parse_data(resp, website, title_selector, chapters_selector, chapterlinks_selector)

    return {
        "website": website,
        "manhwa_data": manhwa_data[:10],    
    }

def parse_data(resp, website, title_selector, chapters_selector, chapterslink_selector=None):
    html = HTMLParser(resp.text)
    titles = [
        element.attributes.get('title', '').strip()
        for element in html.css(title_selector)
    ]
    items = html.css(chapters_selector)
    chapters = [item.text().strip() for item in items]

    if(chapterslink_selector):
        chapters_links = [
            element.attributes.get('href', '').strip()
            for element in html.css(chapterslink_selector)
            if "title" not in element.attributes
        ]
    else:
        chapters_links = [
            element.attributes.get('href', '').strip()
            for element in html.css(chapters_selector)
        ]

    manhwa_data = []
    for i, title in enumerate(titles):
        manhwa_data.append({
            "title": title,
            "chapters": chapters[i * 3: (i + 1) * 3],
            "chapters_links": chapters_links[i * 3: (i + 1) * 3]
        })

    return manhwa_data

if __name__ == "__main__":
    port = 8000
    app.run(port=port)
