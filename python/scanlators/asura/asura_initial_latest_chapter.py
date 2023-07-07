from helpers.get_chapter_number import get_chapter_number

from bs4 import BeautifulSoup


def asura_initial_latest_chapter(resp, selectors):
    soup = BeautifulSoup(resp.text, 'lxml')
    manhwa_data = []

    uta_divs = soup.select('div.uta')

    for div in uta_divs:
        title = div.select_one(selectors["title_selector"]).get(
            'title', '').strip()

        first_chapter_item = div.select_one(selectors["chapters_selector"])
        if first_chapter_item is not None:
            first_chapter = get_chapter_number(
                first_chapter_item.get_text().strip())
        else:
            first_chapter = 0

        manhwa_data.append({
            "title": title,
            "latest_chapter": first_chapter,
        })

    return manhwa_data
