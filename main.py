import time
from barcode_scanner import BarcodeScanner
from book_api import BookAPI
from database import Database
from kiosk_logic import KioskLogic

def main():
    scanner = BarcodeScanner()
    book_api = BookAPI()
    db = Database('books.db')
    kiosk = KioskLogic(scanner, book_api, db)

    print("Book Exchange Kiosk is ready!")
    
    while True:
        try:
            kiosk.process_transaction()
            time.sleep(1)  # Small delay to prevent constant polling
        except KeyboardInterrupt:
            print("\nShutting down kiosk...")
            break

if __name__ == "__main__":
    main()
