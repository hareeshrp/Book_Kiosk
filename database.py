import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                isbn TEXT UNIQUE,
                title TEXT,
                author TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        self.conn.commit()

    def add_book(self, isbn, title, author):
        self.cursor.execute('''
            INSERT OR IGNORE INTO books (isbn, title, author)
            VALUES (?, ?, ?)
        ''', (isbn, title, author))
        self.conn.commit()
        return self.cursor.lastrowid

    def log_transaction(self, book_id, action):
        self.cursor.execute('''
            INSERT INTO transactions (book_id, action)
            VALUES (?, ?)
        ''', (book_id, action))
        self.conn.commit()

    def get_book_balance(self):
        self.cursor.execute('''
            SELECT COUNT(*) FROM transactions
            WHERE action = 'deposit'
        ''')
        deposits = self.cursor.fetchone()[0]
        
        self.cursor.execute('''
            SELECT COUNT(*) FROM transactions
            WHERE action = 'withdraw'
        ''')
        withdrawals = self.cursor.fetchone()[0]
        
        return deposits - withdrawals
