from helpers.get_chapter_number import get_chapter_number

from bs4 import BeautifulSoup


def asura_initial_latest_chapter(resp, selectors):
    soup = BeautifulSoup(resp.text, 'lxml')
    titles = [element.get('title', '').strip()
              for element in soup.select(selectors["title_selector"])]

    chapter_items = soup.select(selectors["chapters_selector"])
    chapters = [item.get_text().strip() for item in chapter_items]

    manhwa_data = []
    for i, title in enumerate(titles):
        latest_chapter = 0 if i >= len(
            chapters) else get_chapter_number(chapters[i])
        manhwa_data.append({
            "title": title,
            "latest_chapter": latest_chapter,
        })

    return manhwa_data
