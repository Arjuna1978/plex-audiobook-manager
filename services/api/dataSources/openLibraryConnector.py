import requests

def getBookDetails(book_name: str):
    # 1. Provide the string exactly as you want it read (e.g., "John Smith")
    # 2. 'params' automatically encodes the spaces into the URL format
    base = "https://openlibrary.org/search.json"
    response = requests.get(base, params={'q': book_name})
    
    # This will return the actual JSON results from OpenLibrary
    return response.json()