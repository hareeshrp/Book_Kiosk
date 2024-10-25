import requests

class BookAPI:
    def __init__(self, api_url=None, api_key=None):
        self.base_url = api_url or "https://openlibrary.org/api/books"
        self.api_key = api_key

    def get_book_info(self, isbn):
        params = {
            "bibkeys": f"ISBN:{isbn}",
            "format": "json",
            "jscmd": "data"
        }
        if self.api_key:
            params['key'] = self.api_key
        
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            book_data = data.get(f"ISBN:{isbn}")
            if book_data:
                return {
                    "title": book_data.get("title"),
                    "author": book_data.get("authors", [{}])[0].get("name"),
                    "isbn": isbn
                }
        return None
