import time
from barcode_scanner import BarcodeScanner
from book_api import BookAPI
from database import Database
from kiosk_logic import KioskLogic

def populate_test_data(db, book_api):
    # Sample ISBNs
    isbns = ['9780061120084', '9780743273565', '9780141439518']
    
    for isbn in isbns:
        book_info = book_api.get_book_info(isbn)
        if book_info:
            book_id = db.add_book(book_info['isbn'], book_info['title'], book_info['author'])
            # Simulate a deposit for each book
            db.log_transaction(book_id, 'deposit')
            print(f"Added test book: {book_info['title']} by {book_info['author']}")
    
    print("Test data populated successfully.")

def main():
    # Configuration
    api_url = "https://openlibrary.org/api/books"  # You can change this to a different API if needed
    api_key = None  # Add your API key here if required

    scanner = BarcodeScanner()
    book_api = BookAPI(api_url, api_key)
    db = Database('books.db')
    kiosk = KioskLogic(book_api, db)

    print("Book Exchange Kiosk is ready!")
    print("Do you want to populate the database with test data? (y/n)")
    if input().lower() == 'y':
        populate_test_data(db, book_api)

    print("Press 'v' to view database contents, or scan a barcode to process a transaction.")
    print("Press 'q' to quit.")
    
    while True:
        print("\nWaiting for input or barcode scan...")
        try:
            barcode = scanner.read_barcode(timeout=0.1)
            
            if barcode:
                print(f"Barcode scanned: {barcode}")
                print(f"Barcode type: {type(barcode)}")
                print(f"Barcode length: {len(barcode)}")
                
                # Test the barcode directly with the book API
                test_book_info = book_api.get_book_info(barcode)
                if test_book_info:
                    print(f"Book API test successful. Book info: {test_book_info}")
                else:
                    print("Book API test failed. No book info found.")
                
                kiosk.process_transaction(barcode)
            elif barcode is None:
                user_input = input().lower()
                if user_input == 'v':
                    db.print_database_contents()
                elif user_input == 'q':
                    print("\nShutting down kiosk...")
                    break
                elif user_input:
                    print("Invalid input. Please try again.")
            else:
                print("Invalid barcode scanned. Please try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
