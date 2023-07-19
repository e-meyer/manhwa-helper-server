from bs4 import BeautifulSoup
import re

from helpers.get_smaller_cover_url import get_smaller_cover_url


def flame_initial_data(resp, selectors):
    soup = BeautifulSoup(resp.text, 'html.parser')

    latest_divs = soup.select('div.latest-updates > div.bs')

    manhwa_data = []

    for div in latest_divs:
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

        # Status label
        status = div.select_one("div.imptdt > div.status")
        status = status.get_text().strip()

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
            "status": status,
            "cover_url": cover_url
        }

        if smaller_cover_url != cover_url:
            data["smaller_cover_url"] = cover_url

        manhwa_data.append(data)

    return manhwa_data

