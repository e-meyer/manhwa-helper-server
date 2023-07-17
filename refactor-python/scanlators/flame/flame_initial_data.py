from bs4 import BeautifulSoup
import re


def flame_initial_data(resp, selectors):
    soup = BeautifulSoup(resp.text, 'html.parser')

    latest_divs = soup.select('div.latest-updates > div.bs')
    test = []
    for div in latest_divs:
        page_url = soup.select_one(selectors["manhwa_page_url_selector"])

        title = soup.select_one(selectors["title_selector"]).get_text().strip()

        cover_url = soup.select_one(selectors["cover_url_selector"])

        cover_url = cover_url.get('src', '')

        status = soup.find_next("div", class_="status")
        test.append(cover_url)

    print(test)
    return

    page_url = [element.get('href', '').strip()
                for element in soup.select(selectors["manhwa_page_url_selector"])]

    title_elements = soup.select(selectors["title_selector"])
    titles = [title.get_text().strip() for title in title_elements]

    cover_url = [element.get('src', '').strip()
                 for element in soup.select(selectors["cover_url_selector"])]

    status_divs = soup.find_all("div", class_="status")
    status = []

    # chapter_items = soup.select(selectors["chapters_selector"])

    # chapters = [item.get_text().strip()
    #             for item in chapter_items]

    for status_div in status_divs:
        i_tag = status_div.find("i")
        status.append(i_tag.text)

    manhwa_data = []

    for i, title in enumerate(titles):
        if status[i] != "Dropped":
            first_chapter_item = div.select_one(selectors["chapters_selector"])
            if first_chapter_item is not None:
                first_chapter = first_chapter_item.get_text().strip()
            else:
                first_chapter = 0

            cover = cover_url[i]
            pattern = r"-\d{3}x\d{3}"

            new_url = re.sub(pattern, "", cover)

            data = {
                "title": title,
                "page_url": page_url[i],
                "cover_url": new_url,
                "latest_chapter_label": first_chapter
            }

            if new_url != cover_url[i]:
                data["smaller_cover_url"] = cover_url[i]

            manhwa_data.append(data)

    return manhwa_data
