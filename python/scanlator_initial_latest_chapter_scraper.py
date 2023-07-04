from time import sleep

from helpers.file_handler import load_manhwa_data, save_manhwa_data
from helpers.request_scanlator_data import request_scanlator_data
from scanlators.asura.asura_initial_latest_chapter import asura_initial_latest_chapter
from scanlators.flame.flame_initial_latest_chapter import flame_initial_latest_chapter
from scanlators.luminous.luminous_initial_latest_chapter import luminous_initial_latest_chapter
from scanlators.reaper.reaper_initial_latest_chapter import reaper_initial_latest_chapter

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


SCANLATOR_INITIAL_DATA_SELECTOR = {
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


SCANLATOR_INITIAL_DATA_SCRAPER_FUNCTION = {
    "asura": asura_initial_latest_chapter,
    "flame": flame_initial_latest_chapter,
    "luminous": luminous_initial_latest_chapter,
    "reaper": reaper_initial_latest_chapter,
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

        existing_data = load_manhwa_data("data", scanlator)
        new_data = manhwa_data

        new_data_dict = {
            new_item['title']: new_item['latest_chapter'] for new_item in new_data}

        for item in existing_data:
            if item['title'] in new_data_dict:
                item['latest_chapter'] = new_data_dict[item['title']]

        if len(manhwa_data) > 0:
            save_manhwa_data("data/notifications", scanlator, existing_data)


def main():
    call()


if __name__ == "__main__":
    main()
