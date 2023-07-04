import re
from bs4 import BeautifulSoup


def flame_periodical_scraping(resp, selectors):
    soup = BeautifulSoup(resp.text, 'html.parser')

    titles = [element.get_text().strip()
              for element in soup.select(selectors["title_selector"])]

    chapters = [re.findall(r'\d+', item.text.strip())[0]
                for item in soup.select(selectors["chapters_selector"])]

    chapters_urls = [
        element.get('href', '').strip()
        for element in soup.select(selectors["chapters_url_selector"])
        if "title" not in element.attrs
    ]

    cover_url = [element.get('src', '').strip()
                 for element in soup.select(selectors["cover_url_selector"])]

    manhwa_data = []
    for i, title in enumerate(titles):
        if i >= 10:
            break

        cover = cover_url[i]
        pattern = r"-\d{3}x\d{3}"

        new_url = re.sub(pattern, "", cover)

        data_item = {
            "title": title,
            "chapters": chapters[i * 3: (i + 1) * 3],
            "chapters_urls": chapters_urls[i * 3: (i + 1) * 3],
            "cover_url": new_url,
        }

        if new_url != cover_url[i]:
            data_item["smaller_cover_url"] = cover_url[i]

        manhwa_data.append(data_item)

    return manhwa_data
