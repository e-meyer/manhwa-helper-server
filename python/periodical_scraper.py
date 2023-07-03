import json

from helpers.file_handler import load_manhwa_data
from helpers.request_scanlator_data import request_scanlator_data
from scanlators.periodical_scraping.asura import asura_data
from scanlators.periodical_scraping.flame import flame_data

SCANLATORS = [
    "asura",
    "flame"
]


SCANLATOR_URL = {
    "asura": "https://www.asurascans.com/page/1",
    "flame": "https://www.flamescans.org/page/1"
}

SCANLATOR_SELECTOR = {
    "asura": {
        "title_selector": "div.luf > a.series",
        "chapters_selector": "div.luf > ul > li > a"
    },
    "flame": {
        "title_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.info > a > div.tt",
        "chapters_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.chapter-list > a > div.adds > div.epxs",
        "chapters_url_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.chapter-list > a"
    }
}

SCANLATOR_DATA_SCRAPER = {
    "asura": asura_data,
    "flame": flame_data
}


def call():
    result = []
    for item in SCANLATORS:
        try:
            response = request_scanlator_data(
                SCANLATOR_URL[item],
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
                },
            )
        except Exception as e:
            return

        selectors = SCANLATOR_SELECTOR[item]
        data_scraper = SCANLATOR_DATA_SCRAPER[item]

        data = data_scraper(response, selectors)

        existing_data = load_manhwa_data("data/notifications", item)

        existing_data_dict = {d['title']: d for d in existing_data}

        result = get_updated_manhwas(
            data, existing_data_dict, result)

    print(json.dumps(result, indent=2))


def get_updated_manhwas(new_data, existing_data_dict, result):
    for data in new_data:
        if data['title'] in existing_data_dict:
            d1 = existing_data_dict[data['title']]

            latest_chapter = int(d1['latest_chapter'])

            new_chapters_numbers = []
            new_chapters_urls = []

            for i, chapter in enumerate(data['chapters']):
                chapter_number = int(chapter.replace('Chapter ', ''))

                if chapter_number > latest_chapter:
                    new_chapters_urls.append(data['chapters_urls'][i])
                    new_chapters_numbers.append(chapter_number)

            if new_chapters_urls:
                cover_url = d1['cover_url']

                result.append({
                    'title': data['title'],
                    'new_chapters_numbers': new_chapters_numbers,
                    'new_chapters_urls': new_chapters_urls,
                    'cover_url': cover_url,
                })
    return result


def main():
    call()


if __name__ == "__main__":
    main()
