from database.model import *
from app import app 
from datetime import date
from sqlalchemy import event
with app.app_context():

    book  = Book.query.filter_by(id = 1).first()
    section = Section.query.filter(Section.id == 4).first()


    # Define your function to be executed on model changes
    def on_model_change(mapper, connection, target):
        # Your function logic here
        print(f"Model {target.__class__.__name__} with id {target.id} has been changed.")

    # Add event listener to YourModel for 'after_update', 'after_insert', and 'after_delete' events
    # event.listen(Book, 'after_update', on_model_change)
    event.listen(Book, 'after_insert', on_model_change)
    # event.listen(Book, 'after_delete', on_model_change)
    new_book_data = {
        "name": "Book 1",
        "description": "Description of Book 1",
        "author": "Author 1",
        "rating": 4,
        "page_count": 200
    }

    new_book = Book(new_book_data)

    # Adding the new_book to the database session
    db.session.add(new_book)
    print("after adding")
    # Committing the session to save the changes to the database
    db.session.commit()
    print("after committing")