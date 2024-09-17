
def add_books(app, db, Book):
    books_data = [
        {"name": "Book 1", "description": "Description of Book 1", "author": "Author 1", "rating": 4,  "page_count": 200},
        {"name": "Book 2", "description": "Description of Book 2", "author": "Author 2", "rating": 3,  "page_count": 250},
        {"name": "Book 3", "description": "Description of Book 3", "author": "Author 3", "rating": 5,  "page_count": 300},
        {"name": "Book 4", "description": "Description of Book 4", "author": "Author 4", "rating": 4,  "page_count": 180},
        {"name": "Book 5", "description": "Description of Book 5", "author": "Author 5", "rating": 3,  "page_count": 220},
        {"name": "Book 6", "description": "Description of Book 6", "author": "Author 6", "rating": 4,  "page_count": 320},
        {"name": "Book 7", "description": "Description of Book 7", "author": "Author 7", "rating": 5,  "page_count": 280},
        {"name": "Book 8", "description": "Description of Book 8", "author": "Author 8", "rating": 3,  "page_count": 240},
        {"name": "Book 9", "description": "Description of Book 9", "author": "Author 9", "rating": 4,  "page_count": 260},
        {"name": "Book 10", "description": "Description of Book 10", "author": "Author 10", "rating": 5, "page_count": 290}
    ]

    for book_data in books_data:
        db.session.add(Book(**book_data))