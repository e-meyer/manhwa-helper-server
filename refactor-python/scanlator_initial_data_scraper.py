from time import sleep

from helpers.file_handler import save_manhwa_data
from helpers.request_scanlator_data import request_scanlator_data
from scanlators.asura.asura_initial_data import asura_initial_data
from scanlators.flame.flame_initial_data import flame_initial_data
from scanlators.luminous.luminous_initial_data import luminous_initial_data
from scanlators.reaper.reaper_initial_data import reaper_initial_data


SCANLATORS = [
    # "asura",
    # "flame",
    # "luminous",
    "reaper"
]


SCANLATOR_URL = {
    "asura": "https://www.asurascans.com/manga/?page=",
    "flame": "https://flamescans.org/page/",
    "luminous": "https://www.luminousscans.com/series/?page=",
    "reaper": "https://reaperscans.com/latest/comics?page="
}


SCANLATOR_INITIAL_DATA_SELECTOR = {
    "asura": {
        "title_selector": "div.luf > a.series",
        "manhwa_page_url_selector": "div.listupd > div.utao > div.uta > div.luf > a",
        "cover_url_selector": "div.listupd > div.utao > div.uta > div.imgu > a > img",
        "chapters_selector": "div.luf > ul > li:first-child > a"
    },
    "flame": {
        "title_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.info > a > div.tt",
        "manhwa_page_url_selector": "div.latest-updates > div.bs > div.bsx > a",
        "cover_url_selector": "div.latest-updates > div.bs > div.bsx > a > div.limit > img",
        "chapters_selector": "a:first-child > div.adds > div.epxs"
    },
    "luminous": {
        "manhwa_page_url_selector": "div.bsx > a",
        "title_selector": "div.bigor > div.tt",
        "cover_url_selector": "div.limit > img"
    },
    "reaper": {
        "manhwa_page_url_selector": "li > div > a",
        "title_selector": "div > div > p > a",
        "cover_url_selector": "li > div > a > img",
        "chapters_selector": "div.grid > div > div > div > div > a"
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
            print(page_number)
            initial_url = SCANLATOR_URL.get(scanlator)
            url = initial_url + str(page_number)

            try:
                response = request_scanlator_data(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
                    },
                )
            except Exception as e:
                print(e)
                break

            selector = SCANLATOR_INITIAL_DATA_SELECTOR[scanlator]
            scanlator_scraper_function = SCANLATOR_INITIAL_DATA_SCRAPER_FUNCTION[scanlator]

            data_returned = scanlator_scraper_function(response, selector)
            print(data_returned)
            break
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
