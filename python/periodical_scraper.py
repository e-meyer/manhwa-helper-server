import json

from helpers.file_handler import load_manhwa_data
from helpers.request_scanlator_data import request_scanlator_data
from scanlators.asura.asura_periodical_scraping import asura_periodical_scraping
from scanlators.flame.flame_periodical_scraping import flame_periodical_scraping

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
        "chapters_selector": "div.luf > ul > li > a",
        "cover_url_selector": "div.imgu > a.series > img",
        "page_url_selector": "div.imgu > a"
    },
    "flame": {
        "title_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.info > a > div.tt",
        "chapters_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.chapter-list > a > div.adds > div.epxs",
        "chapters_url_selector": "div.latest-updates > div.bs > div.bsx > div.bigor > div.chapter-list > a",
        "cover_url_selector": "div.latest-updates > div.bs > div.bsx > a > div.limit > img",
        "page_url_selector": "div.latest-updates > div.bs > div.bsx > a"
    }
}


SCANLATOR_DATA_SCRAPER = {
    "asura": asura_periodical_scraping,
    "flame": flame_periodical_scraping
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

        existing_data = load_manhwa_data("data", item)

        existing_data_dict = {d['title']: d for d in existing_data}

        result = get_updated_manhwas(
            item, data, existing_data_dict, result)

        update_latest_chapter(item, result)

    print(json.dumps(result, indent=2))


def update_latest_chapter(scanlator_name, new_data):
    for item in new_data:
        file_name = f"data/{scanlator_name}.json"
        with open(file_name, 'r') as f:
            existing_data = json.load(f)

        existing_data_dict = {d['title']: d for d in existing_data}

        for data in new_data:
            print(data['title'])
            if data['title'] in existing_data_dict:
                existing_data_dict[data['title']]['latest_chapter'] = str(
                    max(data['new_chapters_numbers'], default=0))
            else:
                new_title = {
                    'title': data['title'],
                    'page_url': data['page_url'],
                    'cover_url': data['cover_url'],
                    'latest_chapter': str(max(data['new_chapters_numbers'], default=0))
                }
                if 'smaller_cover_url' in data:
                    new_title['smaller_cover_url'] = data['smaller_cover_url']
                existing_data.append(new_title)

        with open(file_name, 'w') as f:
            json.dump(existing_data, f, indent=2)

        with open(f"data/notifications/{scanlator_name}.json", 'w') as f:
            json.dump(new_data, f, indent=2)


def get_updated_manhwas(scanlator_name, new_data, existing_data_dict, result):
    result = []
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
                new_item = {
                    'title': data['title'],
                    'page_url': data['page_url'],
                    'new_chapters_numbers': new_chapters_numbers,
                    'new_chapters_urls': new_chapters_urls,
                    'cover_url': cover_url,
                }
                if 'smaller_cover_url' in data:
                    new_item['smaller_cover_url'] = data['smaller_cover_url']
                result.append(new_item)
        else:
            new_item = {
                'title': data['title'],
                'page_url': data['page_url'],
                'new_chapters_numbers': data['chapters'],
                'new_chapters_urls': data['chapters_urls'],
                'cover_url': data['cover_url'],
            }
            if 'smaller_cover_url' in data:
                new_item['smaller_cover_url'] = data['smaller_cover_url']
            result.append(new_item)
    return result


def main():
    call()


if __name__ == "__main__":
    main()
