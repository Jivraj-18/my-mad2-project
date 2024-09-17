from database.model import *
from .user import add_users
from .book import add_books
from .section import add_sections
from .book_section import add_book_sections
from .user_book import add_user_book
def add_test_data(app):
    with app.app_context():
        add_users(app, db, User)
        add_books(app, db, Book)
        add_sections(app, db, Section)
        add_book_sections(app,db,Section, Book)
        add_user_book(app, db, User, Book, user_book_association)
        db.session.commit()
