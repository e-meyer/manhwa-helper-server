import re
from bs4 import BeautifulSoup

from helpers.get_chapter_number import get_chapter_number


def flame_initial_latest_chapter(resp, selectors):
    soup = BeautifulSoup(resp.text, 'lxml')
    titles = [element.get_text().strip()
              for element in soup.select(selectors["title_selector"])]

    chapter_items = soup.select(selectors["chapters_selector"])
    print(chapter_items)
    chapters = [int(re.findall(r'\d+', item.text.strip())[0])
                if re.findall(r'\d+', item.text.strip()) else 0
                for item in chapter_items]

    status_divs = soup.find_all("div", class_="status")
    status = []

    for status_div in status_divs:
        i_tag = status_div.find("i")
        status.append(i_tag.text)

    manhwa_data = []

    for i, title in enumerate(titles):
        if status[i] != "Dropped":
            latest_chapter = 0 if i >= len(
                chapters) else chapters[i]

            manhwa_data.append({
                "title": title,
                "latest_chapter": str(latest_chapter),
            })

    return manhwa_data
