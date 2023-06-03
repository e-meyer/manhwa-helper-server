from flask import Flask, jsonify
import httpx
from selectolax.parser import HTMLParser

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_data():
    results = [
        get_data(
            "Asura",
            "https://www.asurascans.com/",
            "a.series",
        ),
        get_data(
            "Flame",
            "https://flamescans.org/",
            "div.info > a > div.tt",
        ),
    ]
    return jsonify(results)

def get_data(website, url, selector):
    resp = httpx.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )
    html = HTMLParser(resp.text)
    if website == "Asura":
        manhwa_titles = [
            element.text().strip()
            for element in html.css(selector)
            if "rel" not in element.attributes
        ]
    else:
        manhwa_titles = [
            element.text().strip()
            for element in html.css(selector)
        ]
    return {
        "website": website,
        "manhwa_titles": manhwa_titles
    }

if __name__ == "__main__":
    app.run()
