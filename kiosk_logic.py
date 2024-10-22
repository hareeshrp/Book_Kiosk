class KioskLogic:
    def __init__(self, scanner, book_api, database):
        self.scanner = scanner
        self.book_api = book_api
        self.db = database

    def process_transaction(self):
        isbn = self.scanner.read_barcode()
        if isbn:
            book_info = self.book_api.get_book_info(isbn)
            if book_info:
                book_id = self.db.add_book(book_info['isbn'], book_info['title'], book_info['author'])
                
                balance = self.db.get_book_balance()
                if balance > 0:
                    action = 'withdraw'
                    print(f"You can take the book: {book_info['title']} by {book_info['author']}")
                else:
                    action = 'deposit'
                    print(f"Thank you for depositing: {book_info['title']} by {book_info['author']}")
                
                self.db.log_transaction(book_id, action)
                print(f"Current book balance: {balance + (1 if action == 'deposit' else -1)}")
            else:
                print("Book information not found. Please try again.")
        else:
            print("No barcode scanned. Please try again.")
