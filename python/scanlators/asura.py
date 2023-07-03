from bs4 import BeautifulSoup
import re


def asura_search_scraper(resp, manhwa_page_url_selector, title_selector, cover_url_selector, chapter_number_selector):
    soup = BeautifulSoup(resp.text, 'html.parser')

    page_url = [element.get('href', '').strip()
                for element in soup.select(manhwa_page_url_selector)]

    items = soup.select(chapter_number_selector)

    chapters = [item.get_text(strip=True) for item in items]

    chapters_links = [
        item.get('href', '').strip()
        for item in items
        if "title" not in item.attrs
    ]

    title_elements = soup.select(title_selector)
    titles = [title.get_text().strip() for title in title_elements]

    items = soup.select(chapter_number_selector)
    chapters = [item.get_text().strip() for item in items]

    cover_url = [element.get('src', '').strip()
                 for element in soup.select(cover_url_selector)]

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

            if chapters and i < len(chapters):
                numbers = re.findall(r'\d+', chapters[i])
                data["chapters"] = numbers[0] if numbers else ''

            manhwa_data.append(data)

    return manhwa_data
