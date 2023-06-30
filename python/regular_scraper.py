import json
import os
import re
import requests
from time import sleep
from bs4 import BeautifulSoup


def asura():
    page_number = 1
    manhwa_data = []

    while True:
        url = "https://www.asurascans.com/page/" + str(page_number)

        try:
            response = request_scanlator_data(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
                },
            )

        except Exception as e:
            break

        data_returned = parse_data(
            response,
            title_selector="div.luf > a.series",
            chapters_selector="div.luf > ul > li:first-child > a"
        )

        if len(data_returned) == 0:
            break

        for item in data_returned:
            manhwa_data.append(item)

        page_number += 1
        sleep(10)

    if len(manhwa_data) > 0:
        save_manhwa_data("asura", manhwa_data)


def request_scanlator_data(url, headers):
    try:
        response = requests.get(
            url,
            headers=headers,
        )
        response.raise_for_status()

        return response
    except requests.exceptions.Timeout as e:
        raise Exception(f"Request timed out: {str(e)}")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def parse_data(resp, title_selector, chapters_selector):
    soup = BeautifulSoup(resp.text, 'lxml')
    titles = [element.get('title', '').strip()
              for element in soup.select(title_selector)]

    chapter_items = soup.select(chapters_selector)

    chapters = [item.get_text().strip() for item in chapter_items]

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
        latest_chapter = 0 if chapters[i] is None else get_chapter_number(
            chapters[i])
        manhwa_data.append({
            "title": title,
            "latest_chapter": latest_chapter,
        })

    return manhwa_data


def save_manhwa_data(file_name, data):
    output_file_path = os.path.join("data/notifications", file_name + ".json")
    with open(output_file_path, "w") as json_file:
        json.dump(data, json_file)


def get_chapter_number(title):
    match = re.search(r'Chapter (\d+)', title)
    if match:
        return match.group(1)
    else:
        return None


asura()
