import json
from bs4 import BeautifulSoup


def reaper_periodical_scraping(resp, selectors):
    soup = BeautifulSoup(resp.text, 'lxml')
    titles = [element.get_text().strip()
              for element in soup.select(selectors["title_selector"])]

    page_url = [element.get('href', '').strip()
                for element in soup.select(selectors["page_url_selector"])]

    chapters = [
        element.get_text().strip()
        for element in soup.select(selectors["chapters_selector"])
    ]

    chapters_urls = [
        element.get('href', '').strip()
        for element in soup.select(selectors["chapters_selector"])
    ]

    cover_url = [element.get('src', '').strip()
                 for element in soup.select(selectors["cover_url_selector"])]

    manhwa_data = []
    for i, title in enumerate(titles):
        if i >= 10:
            break
        manhwa_data.append({
            "title": title,
            "page_url": page_url[i],
            "chapters": chapters[i * 2: (i + 1) * 2],
            "chapters_urls": chapters_urls[i * 2: (i + 1) * 2],
            "cover_url": cover_url[i]
        })
        
    return manhwa_data
