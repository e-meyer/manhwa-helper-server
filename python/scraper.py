from flask import Flask, jsonify
import httpx
from selectolax.parser import HTMLParser
import threading

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_data():
    # Create a list to hold the threads
    threads = []

    # Create a function to handle each get_data call in a separate thread
    def scrape_website(website, url, selector):
        result = get_data(website, url, selector)
        results.append(result)

    # Create a list to store the results
    results = []

    # Start a thread for each website
    t1 = threading.Thread(target=scrape_website, args=("Asura", "https://www.asurascans.com/", "a.series"))
    threads.append(t1)
    t1.start()

    t2 = threading.Thread(target=scrape_website, args=("Flame", "https://flamescans.org/", "div.info > a > div.tt"))
    threads.append(t2)
    t2.start()

    t3 = threading.Thread(target=scrape_website, args=("Luminous", "https://luminousscans.com/", "div.luf > a.series"))
    threads.append(t3)
    t3.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

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
    elif website == "Luminous":
        manhwa_titles = [
            element.attributes.get('title', '').strip()
            for element in html.css(selector)
        ]
    else:
        manhwa_titles = [
            element.text().strip()
            for element in html.css(selector)
        ]
    return {
        "website": website,
        "manhwa_titles": manhwa_titles[:10]
    }

if __name__ == "__main__":
    app.run()
