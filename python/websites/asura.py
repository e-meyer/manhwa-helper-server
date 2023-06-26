from bs4 import BeautifulSoup
import re

def asura_search_scraper(resp, manhwa_page_url_selector, title_selector, cover_url_selector, chapter_number_selector):
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    page_url = [element.get('href', '').strip() for element in soup.select(manhwa_page_url_selector)]

    title_elements = soup.select(title_selector)
    titles = [title.get_text().strip() for title in title_elements]

    items = soup.select(chapter_number_selector)
    chapters = [item.get_text().strip() for item in items]

    cover_url = [element.get('src', '').strip() for element in soup.select(cover_url_selector)]

    manhwa_data = []

    for i, title in enumerate(titles):
        data = {
            "title": title,
            "page_url": page_url[i],
            "cover_url": cover_url[i],
        }

        if chapters and i < len(chapters):
            numbers = re.findall(r'\d+', chapters[i])
            data["chapters"] = numbers[0] if numbers else ''

        manhwa_data.append(data)

    return manhwa_data