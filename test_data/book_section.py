def add_book_sections(app, db, Section, Book):
    for i in range(0, 5):
        book = Book.query.filter_by(id=1+i).first()
        section = Section.query.filter_by(id=10-i).first()
        book.sections.append(section)