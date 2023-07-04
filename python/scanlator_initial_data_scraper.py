from time import sleep

from helpers.file_handler import save_manhwa_data
from helpers.request_scanlator_data import request_scanlator_data
from scanlators.asura.asura_initial_data import asura_initial_data
from scanlators.flame.flame_initial_data import flame_initial_data
from scanlators.luminous.luminous_initial_data import luminous_initial_data
from scanlators.reaper.reaper_initial_data import reaper_initial_data


SCANLATORS = [
    "asura",
    "flame",
    "luminous",
    "reaper"
]


SCANLATOR_URL = {
    "asura": "https://www.asurascans.com/manga/?page=",
    "flame": "https://flamescans.org/series/?page=",
    "luminous": "https://www.luminousscans.com/series/?page=",
    "reaper": "https://reaperscans.com/comics?page="
}


SCANLATOR_INITIAL_DATA_SELECTOR = {
    "asura": {
        "manhwa_page_url_selector": "div.bsx > a",
        "title_selector": "div.bigor > div.tt",
        "cover_url_selector": "div.limit > img"
    },
    "flame": {
        "manhwa_page_url_selector": "div.bsx > a",
        "title_selector": "div.bigor > div.tt",
        "cover_url_selector": "div.limit > img"
    },
    "luminous": {
        "manhwa_page_url_selector": "div.bsx > a",
        "title_selector": "div.bigor > div.tt",
        "cover_url_selector": "div.limit > img"
    },
    "reaper": {
        "manhwa_page_url_selector": "li > div > a",
        "title_selector": "li > div > ",
        "cover_url_selector": "li > div > a > img"
    }
}


SCANLATOR_INITIAL_DATA_SCRAPER_FUNCTION = {
    "asura": asura_initial_data,
    "flame": flame_initial_data,
    "luminous": luminous_initial_data,
    "reaper": reaper_initial_data,
}


def call():
    for scanlator in SCANLATORS:
        page_number = 1
        manhwa_data = []

        while True:
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

            selector = SCANLATOR_INITIAL_DATA_SELECTOR[scanlator]
            scanlator_scraper_function = SCANLATOR_INITIAL_DATA_SCRAPER_FUNCTION[scanlator]

            data_returned = scanlator_scraper_function(response, selector)

            if len(data_returned) == 0:
                break

            for item in data_returned:
                manhwa_data.append(item)

            

            page_number += 1
            sleep(5)

        save_manhwa_data("data", scanlator, manhwa_data)


def main():
    call()


if __name__ == "__main__":
    main()
