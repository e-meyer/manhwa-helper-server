from bs4 import BeautifulSoup
import re


def asura_data(resp, selectors):
    soup = BeautifulSoup(resp.text, 'html.parser')

    titles = [element.get('title', '').strip()
              for element in soup.select(selectors["title_selector"])]

    chapters = [re.findall(r'\d+', item.text.strip())[0]
                for item in soup.select(selectors["chapters_selector"])]

    chapters_urls = [
        element.get('href', '').strip()
        for element in soup.select(selectors["chapters_selector"])
        if "title" not in element.attrs
    ]

    manhwa_data = []
    for i, title in enumerate(titles):
        if i >= 10:
            break
        manhwa_data.append({
            "title": title,
            "chapters": chapters[i * 3: (i + 1) * 3],
            "chapters_urls": chapters_urls[i * 3: (i + 1) * 3],
        })

    return manhwa_data


# def asura_data(resp, title_selector, chapters_selector):
#     soup = BeautifulSoup(resp.text, 'html.parser')

#     titles = [element.get('title', '').strip()
#               for element in soup.select(title_selector)]

#     chapters = [re.findall(r'\d+', item.text.strip())[0]
#                 for item in soup.select(chapters_selector)]

#     chapters_urls = [
#         element.get('href', '').strip()
#         for element in soup.select(chapters_selector)
#         if "title" not in element.attrs
#     ]

#     manhwa_data = []
#     for i, title in enumerate(titles):
#         if i >= 10:
#             break
#         manhwa_data.append({
#             "title": title,
#             "chapters": chapters[i * 3: (i + 1) * 3],
#             "chapters_urls": chapters_urls[i * 3: (i + 1) * 3],
#         })

#     return manhwa_data
