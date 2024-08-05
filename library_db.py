import sqlite3
import os

# Define the path for the database file
db_path = os.path.join(os.getcwd(), 'library.db')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# SQL commands to create tables
create_tables_sql = """
CREATE TABLE IF NOT EXISTS Authors (
    author_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id)
);

CREATE TABLE IF NOT EXISTS Borrowers (
    borrower_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS BorrowedBooks (
    borrow_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    borrower_id INTEGER,
    borrow_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id),
    FOREIGN KEY (borrower_id) REFERENCES Borrowers(borrower_id)
);
"""

# Execute the SQL commands
cursor.executescript(create_tables_sql)
conn.commit()

# Data Insertion Functions
def insert_author(author_id, name):
    cursor.execute("INSERT INTO Authors (author_id, name) VALUES (?, ?)", (author_id, name))
    conn.commit()

def insert_book(book_id, title, author_id):
    cursor.execute("INSERT INTO Books (book_id, title, author_id) VALUES (?, ?, ?)", (book_id, title, author_id))
    conn.commit()

def insert_borrower(borrower_id, name):
    cursor.execute("INSERT INTO Borrowers (borrower_id, name) VALUES (?, ?)", (borrower_id, name))
    conn.commit()

def insert_borrowed_book(borrow_id, book_id, borrower_id, borrow_date, return_date):
    cursor.execute("INSERT INTO BorrowedBooks (borrow_id, book_id, borrower_id, borrow_date, return_date) VALUES (?, ?, ?, ?, ?)",
                   (borrow_id, book_id, borrower_id, borrow_date, return_date))
    conn.commit()

# Data Retrieval Functions
def get_all_books():
    cursor.execute("SELECT * FROM Books")
    return cursor.fetchall()

def get_books_by_author(author_id):
    cursor.execute("SELECT * FROM Books WHERE author_id = ?", (author_id,))
    return cursor.fetchall()

def get_borrowed_books():
    cursor.execute("""
    SELECT Books.title, Borrowers.name, BorrowedBooks.borrow_date, BorrowedBooks.return_date
    FROM BorrowedBooks
    JOIN Books ON BorrowedBooks.book_id = Books.book_id
    JOIN Borrowers ON BorrowedBooks.borrower_id = Borrowers.borrower_id
    """)
    return cursor.fetchall()

# Create indexes to speed up queries
cursor.execute("CREATE INDEX idx_author_id ON Books (author_id)")
cursor.execute("CREATE INDEX idx_borrower_id ON BorrowedBooks (borrower_id)")
conn.commit()

# Insert sample data
insert_author(1, 'Author A')
insert_author(2, 'Author B')
insert_book(1, 'Book 1', 1)
insert_book(2, 'Book 2', 1)
insert_book(3, 'Book 3', 2)
insert_borrower(1, 'Borrower 1')
insert_borrowed_book(1, 1, 1, '2024-01-01', '2024-01-15')

# Retrieve and print data
print("All books:", get_all_books())
print("Books by author 1:", get_books_by_author(1))
print("Borrowed books:", get_borrowed_books())

# Always close the database connection when done
conn.close()
