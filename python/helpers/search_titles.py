def search_titles(query, data):
    results = []
    query_words = query.lower().split()
    for item in data:
        title_words = item["title"].lower().split()
        if all(any(query_word in title_word for title_word in title_words) for query_word in query_words):
            results.append(item)
    return results
