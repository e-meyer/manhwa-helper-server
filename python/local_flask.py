from flask import Flask
from flask import request
from bs4 import BeautifulSoup
import requests

from websites.asura import asura_search_scraper
from websites.flame import flame_search_scraper
from websites.luminous import luminous_search_scraper
from websites.reaper import reaper_search_scraper

app = Flask(__name__)


@app.route('/asura', methods=['GET'])
def asura():
    query = request.args.get('query')
    url = "https://asurascans.com/?s=" + query

    response = request_website_data(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )

    manhwa_data = asura_search_scraper(
        response,
        manhwa_page_url_selector="div.bsx > a",
        title_selector="div.bigor > div.tt",
        cover_url_selector="div.limit > img",
        chapter_number_selector="div.epxs",
    )

    return {
        "website": "Asura",
        "manhwa_data": manhwa_data
    }


@app.route('/luminous', methods=['GET'])
def luminous():
    query = request.args.get('query')
    url = "https://luminousscans.com/?s=" + query

    response = request_website_data(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )

    manhwa_data = luminous_search_scraper(
        response,
        manhwa_page_url_selector="div.bsx > a",
        title_selector="div.bigor > div.tt",
        cover_url_selector="div.limit > img",
        chapter_number_selector="div.epxs",
    )

    return {
        "website": "Luminous",
        "manhwa_data": manhwa_data
    }


@app.route('/flame', methods=['GET'])
def flame():
    query = request.args.get('query')
    url = "https://flamescans.org/?s=" + query

    response = request_website_data(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )

    manhwa_data = flame_search_scraper(
        response,
        manhwa_page_url_selector="div.bsx > a",
        title_selector="div.bigor > div.tt",
        cover_url_selector="div.limit > img",
        chapter_number_selector="div.epxs",
    )

    return {
        "website": "Flame",
        "manhwa_data": manhwa_data
    }


@app.route('/reaper', methods=['GET'])
def reaper():
    query = request.args.get('query')
    url = "https://reaperscans.com/"

    response = request_website_data(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )

    manhwa_data = reaper_search_scraper(response, query)

    return {
        "website": "Reaper",
        "manhwa_data": manhwa_data,
    }


def request_website_data(url, headers):
    try:
        response = requests.get(
            url,
            headers=headers,
        )
        response.raise_for_status()

        return response
    except requests.exceptions.Timeout as e:
        raise Exception(f"Request timed out: {str(e)}")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
