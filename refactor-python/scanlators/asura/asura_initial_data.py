from bs4 import BeautifulSoup
import re

from helpers.get_smaller_cover_url import get_smaller_cover_url


def asura_initial_data(resp, selectors):
    soup = BeautifulSoup(resp.text, 'html.parser')

    uta_divs = soup.select('div.uta')

    manhwa_data = []

    for div in uta_divs:
        # Title
        title = div.select_one(selectors["title_selector"])
        title = title.get_text().strip()

        # Page URL
        page_url = div.select_one(selectors["manhwa_page_url_selector"])
        page_url = page_url.get('href', '')

        # Cover URL
        cover_url = div.select_one(selectors["cover_url_selector"])
        cover_url = cover_url.get('src', '')
        smaller_cover_url = get_smaller_cover_url(cover_url)

        # Latest chapter
        latest_chapter_label = div.select_one(selectors["chapters_selector"])
        if latest_chapter_label is not None:
            latest_chapter = latest_chapter_label.get_text().strip()
        else:
            latest_chapter = 'No chapters yet'

        data = {
            "title": title,
            "page_url": page_url,
            "latest_chapter_label": latest_chapter,
            "cover_url": cover_url
        }

        if smaller_cover_url != cover_url:
            data["smaller_cover_url"] = cover_url

        manhwa_data.append(data)

    return manhwa_data

    page_url = [element.get('href', '').strip()
                for element in soup.select(selectors["manhwa_page_url_selector"])]

    title_elements = soup.select(selectors["title_selector"])
    titles = [title.get_text().strip() for title in title_elements]

    cover_url = [element.get('src', '').strip()
                 for element in soup.select(selectors["cover_url_selector"])]

    status_spans = soup.find_all("span", class_="status")
    dropped_titles = []

    for status_span in status_spans:
        parent_div = status_span.find_parent("div", class_="limit")
        sibling_div = parent_div.find_next_sibling("div", class_="bigor")
        child_div = sibling_div.find("div", class_="tt")
        dropped_title = child_div.text.strip()
        dropped_titles.append(dropped_title)

    manhwa_data = []

    for i, title in enumerate(titles):
        if title not in dropped_titles:
            cover = cover_url[i]
            pattern = r"-\d{3}x\d{3}"

            new_url = re.sub(pattern, "", cover)

            data = {
                "title": title,
                "page_url": page_url[i],
                "cover_url": new_url,
            }

            if new_url != cover_url[i]:
                data["smaller_cover_url"] = cover_url[i]

            manhwa_data.append(data)

    return manhwa_data
