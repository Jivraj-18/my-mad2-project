def add_user_book(app,db,User, Book, user_book_association):
    for i in range(0,5):
        user = User.query.filter_by(id=1+i).first()
        book = Book.query.filter_by(id=10-i).first()
        user_book_association_data = {
            'book_id': book.id,
            'user_id': user.id
        }

        # Add the data to the association table
        db.session.execute(user_book_association.insert().values(**user_book_association_data))

        # Commit the session to persist the changes
        db.session.commit()