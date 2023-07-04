import json
import os
import re
import requests
from time import sleep
from bs4 import BeautifulSoup

from get_active_manhwa_list import request_scanlator_data
from helpers.file_handler import load_manhwa_data, save_manhwa_data
from scanlators.initial_scraping.asura import asura_data
from scanlators.initial_scraping.flame import flame_data
from scanlators.initial_scraping.luminous import luminous_data
from scanlators.initial_scraping.reaper import reaper_data

SCANLATORS = [
    "asura",
    "flame",
    "luminous",
    "reaper"
]


SCANLATOR_URL = {
    "asura": "https://www.asurascans.com/page/",
    "flame": "https://www.flamescans.org/page/",
    "luminous": "https://www.luminousscans.com/page/",
    "reaper": "https://reaperscans.com/latest/comics?page="
}


SCANLATOR_SELECTOR = {
    "asura": {
        "title_selector": "div.luf > a.series",
        "chapters_selector": "div.luf > ul > li:first-child > a"
    },
    "flame": {
        "title_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.info > a > div.tt",
        "chapters_selector": "a:first-child > div.adds > div.epxs"
    },
    "luminous": {
        "title_selector": "div.luf > a.series",
        "chapters_selector": "div.luf > ul > li:first-child > a"
    },
    "reaper": {
        "title_selector": "div > div > p > a",
        "chapters_selector": "div.grid > div > div > div > div > a:first-child"
    }
}


SCANLATOR_DATA_SCRAPER = {
    "asura": asura_data,
    "flame": flame_data,
    "luminous": luminous_data,
    "reaper": reaper_data,
}

def call():
    for scanlator in SCANLATORS:
        page_number = 1
        manhwa_data = []

        while True:
            print(page_number)
            initial_url = SCANLATOR_URL.get(scanlator)
            url = initial_url + str(page_number)

            try:
                response = request_scanlator_data(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
                    },
                )
            except Exception as e:
                break

            selectors = SCANLATOR_SELECTOR[scanlator]
            data_scraper = SCANLATOR_DATA_SCRAPER[scanlator]
            
            data_returned = data_scraper(response, selectors)

            if len(data_returned) == 0:
                break

            for item in data_returned:
                manhwa_data.append(item)

            page_number += 1
            sleep(5)

        
        data1 = load_manhwa_data("data", scanlator)
        data2 = manhwa_data
        
        data2_dict = {d['title']: d['latest_chapter'] for d in data2}

        for d1 in data1:
            if d1['title'] in data2_dict:
                d1['latest_chapter'] = data2_dict[d1['title']]

        if len(manhwa_data) > 0:
            save_manhwa_data("data/notifications", scanlator, data1)


def main():
    call()


if __name__ == "__main__":
    main()
