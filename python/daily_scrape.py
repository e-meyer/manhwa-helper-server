import json
import os
from flask import jsonify
from bs4 import BeautifulSoup
import requests
from time import sleep

from scanlators.asura import asura_search_scraper
from scanlators.flame import flame_search_scraper
from scanlators.luminous import luminous_search_scraper
from scanlators.reaper import reaper_search_scraper


def asura():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://www.asurascans.com/manga/?page=" + str(page_number)

        response = request_scanlator_data(
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
        sleep(5)

    save_manhwa_data("asura", manhwa_data)

    return manhwa_data


def flame():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://flamescans.org/series/?page=" + str(page_number)

        response = request_scanlator_data(
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
        sleep(5)

    save_manhwa_data("flame", manhwa_data)

    return manhwa_data


def reaper():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://reaperscans.com/comics?page=" + str(page_number)

        response = request_scanlator_data(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
            },
        )

        data_returned = reaper_search_scraper(
            response,
            manhwa_page_url_selector="li > div > a",
            title_selector="li > div > ",
            cover_url_selector="li > div > a > img",
            chapter_number_selector="div.epxs",
        )

        if len(data_returned) == 0:
            break

        for item in data_returned:
            manhwa_data.append(item)

        page_number += 1
        sleep(10)

    scraped_data = {
        "scanlator": "Reaper",
        "manhwa_data": manhwa_data
    }

    save_manhwa_data("reaper", scraped_data)

    return scraped_data


def luminous():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://www.luminousscans.com/series/?page=" + str(page_number)

        response = request_scanlator_data(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
            },
        )

        data_returned = luminous_search_scraper(
            response,
            manhwa_page_url_selector="div.bsx > a",
            title_selector="div.bigor > div.tt",
            cover_url_selector="div.limit > img",
            chapter_number_selector="div.epxs",
        )

        if len(data_returned) == 0:
            break

        for item in data_returned:
            manhwa_data.append(item)

        page_number += 1
        sleep(10)

    scraped_data = {
        "scanlator": "Luminous",
        "manhwa_data": manhwa_data
    }

    save_manhwa_data("luminous", scraped_data)

    return scraped_data


def request_scanlator_data(url, headers):
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


def save_manhwa_data(file_name, data):
    output_file_path = os.path.join("data", file_name + ".json")
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file)


def main():
    asura()
    print('done scraping asura')
    # luminous()
    # print('done scraping lumi')
    flame()
    print('done scraping flame')
    # reaper()
    # print('done scraping reaper')


if __name__ == "__main__":
    main()
