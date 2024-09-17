from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table,Column, Integer, ForeignKey, String,CheckConstraint, Boolean
from sqlalchemy.orm import relationship
db = SQLAlchemy()

import datetime
book_section_association = Table(
    'book_section_association',
    db.Model.metadata,
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
    Column('section_id', Integer, ForeignKey('section.id'), primary_key=True),
)
user_book_association = Table('user_book_association', db.Model.metadata,
    Column('user_id', db.Integer, ForeignKey('user.id'), primary_key=True),
    Column('book_id', db.Integer, ForeignKey('book.id'), primary_key=True),
    Column('rating', db.Integer),
    Column('rating_description', db.String),
    Column('rated_date', db.Date ),
    Column('status', db.Integer, default=0) , # pending --> 0, accepted --> 1 , rejected --> 2, returned --> 3, revoked --> 4
    Column('request_date',db.Date, default=datetime.datetime.now),
    Column('request_expiry_date', db.Date),
    Column('previously_read', db.Boolean, default = False),
    CheckConstraint('status >= 0 AND status <= 4', name='status_constraint')
)


def user_book_association_to_dict(row):
    association_dict = {}
    columns = ['user_id', 'book_id', 'rating', 'rating_description', 'rated_date', 'status', 'request_date', 'request_expiry_date','previously_read']
    for index, column_value in enumerate(row):
        column_name = columns[index]
        if isinstance(column_value, datetime.date):
            # Convert date objects to string using isoformat()
            column_value = column_value.isoformat()
        association_dict[column_name] = column_value
    # print(association_dict['book_id'])
    association_dict['book_details'] = (Book.query.filter(Book.id == association_dict["book_id"]).first()).to_dict()
    association_dict['user_details'] = (User.query.filter(User.id == association_dict["user_id"]).first()).to_dict()
    return association_dict



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(255) ); l_name = db.Column(db.String(255),default='')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, default=1) # 0 --> admin and 1 --> user
    last_visited = db.Column(db.Date, default=datetime.datetime.now)
    verified = db.Column(db.Boolean, default=False)
    request_count = db.Column(db.Integer, default=0)
    books = relationship("Book", secondary=user_book_association, back_populates="users",)
    requested_books = db.Column(db.Integer, default=0)
    __table_args__ = (
        CheckConstraint('requested_books<=5', name="max_allowed_books"),
    )
    def to_dict(self):
        return {
            'id': self.id,
            'f_name': self.f_name,
            'l_name': self.l_name,
            'email': self.email,
            'role': self.role,
            'last_visited': self.last_visited.isoformat(),
           'verified': self.verified,
           'request_count': self.request_count,
            'books': [book.to_dict() for book in self.books],
           'requested_books': self.requested_books,
        }

# Section Model
class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.Date(), default=datetime.datetime.now)
    description = db.Column(db.String(), nullable=False)
    books_count = db.Column(db.Integer, default=0)
    books = relationship("Book", secondary=book_section_association, back_populates="sections", cascade="all, delete")
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created.isoformat(),
            'description': self.description,
            'books_count': self.books_count,
        }
# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False) # create multiple authors
    rating = db.Column(db.Integer(), nullable=True)
    sections = relationship("Section", secondary=book_section_association, back_populates="books")
    users = relationship("User", secondary=user_book_association, back_populates="books", cascade="all, delete")
    page_count = db.Column(db.Integer())
    date_added = db.Column(db.Date(), default=datetime.datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'rating': self.rating,
            'page_count': self.page_count,
            'date_added': self.date_added.isoformat()
        }
class AuthorRequest(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


