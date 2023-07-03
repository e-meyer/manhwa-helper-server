import json
from bs4 import BeautifulSoup
import re


def luminous_search_scraper(resp, manhwa_page_url_selector, title_selector, cover_url_selector):
    soup = BeautifulSoup(resp.text, 'html.parser')

    page_url = [element.get('href', '').strip()
                for element in soup.select(manhwa_page_url_selector)]

    title_elements = soup.select(title_selector)
    titles = [title.get_text().strip() for title in title_elements]

    cover_url = [element.get('src', '').strip()
                 for element in soup.select(cover_url_selector)]

    dropped_titles = []

    scripts = soup.find_all('script', type="text/javascript")
    for script in scripts:
        if 'const dropped' in script.text:
            js_code = script.text
            break

    dropped_array_str = re.search(r'const dropped = {[^}]*}', js_code).group()

    titles_str = re.search(r'\[.*\]', dropped_array_str).group()

    titles_str = titles_str[1:-1]
    dropped_titles = [title.strip()[1:-1] for title in titles_str.split(',')]

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
