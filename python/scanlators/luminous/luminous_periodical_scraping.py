from bs4 import BeautifulSoup
import re


def luminous_periodical_scraping(resp, selectors):
    soup = BeautifulSoup(resp.text, 'html.parser')

    titles = [element.get('title', '').strip()
              for element in soup.select(selectors["title_selector"])]

    page_url = [element.get('href', '').strip()
                for element in soup.select(selectors["page_url_selector"])]

    chapters = [re.findall(r'\d+', item.text.strip())[0]
                for item in soup.select(selectors["chapters_selector"])]

    chapters_urls = [
        element.get('href', '').strip()
        for element in soup.select(selectors["chapters_selector"])
        if "title" not in element.attrs
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
            "chapters": chapters[i * 3: (i + 1) * 3],
            "chapters_urls": chapters_urls[i * 3: (i + 1) * 3],
            "cover_url": cover_url[i],
        })

    return manhwa_data
