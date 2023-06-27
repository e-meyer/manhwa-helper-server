from flask import Flask
from flask import request
from bs4 import BeautifulSoup
import requests
from time import sleep

from websites.asura import asura_search_scraper
from websites.flame import flame_search_scraper
from websites.luminous import luminous_search_scraper
from websites.reaper import reaper_search_scraper
# https://www.asurascans.com/manga/?page=1
# https://flamescans.org/series/?page=1
app = Flask(__name__)


@app.route('/asura')
def asura():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://www.asurascans.com/manga/?page=" + str(page_number)

        response = request_website_data(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
            },
        )

        data_returned = asura_search_scraper(
            response,
            manhwa_page_url_selector="div.bsx > a",
            title_selector="div.bigor > div.tt",
            cover_url_selector="div.limit > img",
            chapter_number_selector="div.epxs",
            status_selector="div.limit > div.status",
        )

        if len(data_returned) == 0:
            break

        for item in data_returned:
            manhwa_data.append(item)

        page_number += 1
        sleep(10)

    return {
        "website": "Asura",
        "manhwa_data": manhwa_data
    }


@ app.route('/flame')
def flame():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://flamescans.org/series/?page=" + str(page_number)

        response = request_website_data(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
            },
        )
        data_returned = flame_search_scraper(
            response,
            manhwa_page_url_selector="div.bsx > a",
            title_selector="div.bigor > div.tt",
            cover_url_selector="div.limit > img",
            chapter_number_selector="div.epxs",
            status_selector="div.status > i"
        )

        if len(data_returned) == 0:
            break

        for item in data_returned:
            manhwa_data.append(item)

        page_number += 1
        sleep(10)

    return {
        "website": "Flame",
        "manhwa_data": manhwa_data
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

# @app.route('/luminous', methods=['GET'])
# def luminous():
#     query = request.args.get('query')
#     url="https://luminousscans.com/?s=" + query

#     response = request_website_data(
#         url,
#         headers={
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
#         },
#     )

#     manhwa_data = luminous_search_scraper(
#         response,
#         manhwa_page_url_selector="div.bsx > a",
#         title_selector="div.bigor > div.tt",
#         cover_url_selector="div.limit > img",
#         chapter_number_selector="div.epxs",
#     )

#     return {
#         "website": "Luminous",
#         "manhwa_data": manhwa_data
#     }

# @app.route('/reaper', methods=['GET'])
# def reaper():
#     query = request.args.get('query')
#     url="https://reaperscans.com/"

#     response = request_website_data(
#         url,
#         headers={
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
#         },
#         )

#     manhwa_data = reaper_search_scraper(response, query)

#     return {
#         "website": "Reaper",
#         "manhwa_data": manhwa_data,
#     }
