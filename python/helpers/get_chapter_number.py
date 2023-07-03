import re


def get_chapter_number(title):
    match = re.search(r'Chapter (\d+)', title)
    if match:
        return match.group(1)
    else:
        return None
