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
        
        print(f"Requesting book info for ISBN: {isbn}")
        print(f"URL: {self.base_url}")
        print(f"Params: {params}")
        
        try:
            response = requests.get(self.base_url, params=params)
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response data: {data}")
                book_data = data.get(f"ISBN:{isbn}")
                if book_data:
                    result = {
                        "title": book_data.get("title"),
                        "author": book_data.get("authors", [{}])[0].get("name"),
                        "isbn": isbn
                    }
                    print(f"Extracted book info: {result}")
                    return result
                else:
                    print(f"No book data found for ISBN:{isbn}")
            else:
                print(f"Error response: {response.text}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        return None
