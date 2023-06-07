from flask import Flask, jsonify
from selectolax.parser import HTMLParser
import httpx
import ssl

app = Flask(__name__)


@app.route('/asura_scraper', methods=['GET'])
def scrape_data():
    results = [
        get_data(
            "Asura",
            "https://www.asurascans.com/manga/list-mode/",
            "div.luf > a.series",
            "div.luf > ul > li > a"
        ),
    ]
    return jsonify(results)


def get_data(website, url, title_selector, chapters_selector, chapterlinks_selector, coverlink_selector):
    resp = httpx.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
        verify=ssl.CERT_NONE
    )

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


if __name__ == "__main__":
    app.run()
