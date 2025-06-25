from googlesearch import search

def google_search(query, num_results=5):
    results = []
    for url in search(query, num_results=num_results):
        results.append(url)
    return results
