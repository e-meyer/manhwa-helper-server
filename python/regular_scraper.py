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
            "a.series",
            "div.luf > ul > li > a"
        ),
        get_data(
            "Flame",
            "https://flamescans.org/",
            "div.info > a > div.tt",
            "div.adds > div.epxs"
        ),
        get_data(
            "Luminous",
            "https://luminousscans.com/",
            "div.luf > a.series",
            "div.luf > ul > li > a"
        ),
    ]
    return jsonify(results)

def get_data(website, url, title_selector, chapters_selector):
    resp = httpx.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )
    html = HTMLParser(resp.text)
    if website == "Asura":
        titles = [
            element.text().strip()
            for element in html.css(title_selector)
            if "rel" not in element.attributes
        ]
        items = html.css(chapters_selector)
        chapters = [item.text().strip() for item in items]

        manhwa_data = []
        for i, title in enumerate(titles):
            manhwa_data.append({
                "title": title,
                "chapters": chapters[i * 3: (i + 1) * 3]
            })
    elif website == "Luminous":
        titles = [
            element.attributes.get('title', '').strip()
            for element in html.css(title_selector)
        ]
        items = html.css(chapters_selector)
        chapters = [item.text().strip() for item in items]

        manhwa_data = []
        for i, title in enumerate(titles):
            manhwa_data.append({
                "title": title,
                "chapters": chapters[i * 3: (i + 1) * 3]
            })
    elif website == "Flame":
        titles = [
            element.text().strip()
            for element in html.css(title_selector)
        ]
        items = html.css(chapters_selector)
        chapters = [item.text().strip() for item in items]

        manhwa_data = []
        for i, title in enumerate(titles):
            manhwa_data.append({
                "title": title,
                "chapters": chapters[i * 3: (i + 1) * 3]
            })
    return {
        "website": website,
        "manhwa_data": manhwa_data[:10],    
    }

if __name__ == "__main__":
    port = 8000
    app.run(port=port)
