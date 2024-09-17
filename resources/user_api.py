from flask import request
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.model import *
import os

class CanRequestBook(Resource):
    @jwt_required()
    def __init__(self):
        self.user_id = get_jwt_identity()
    @jwt_required()
    def get(self):
        user = User.query.filter_by(id=self.user_id).first()
        if user.requested_books >= 5 :
            return False, 200
        else :
            return True, 200

class UserIssuedBook(Resource):
    @jwt_required()
    def __init__(self):
        self.user_id = get_jwt_identity()
    @jwt_required()
    def get(self):
        issued_books = db.session.query(user_book_association).filter_by(user_id=self.user_id).all()
        return [user_book_association_to_dict(x) for x in issued_books], 200

    

class UserBookApi(Resource):
    @jwt_required()
    def get(self, book_id=None):
        if book_id :
            book = Book.query.filter_by(id=book_id).first()
            return (book.to_dict(), 200) if book else ("not found", 404)
        else : 
            books = Book.query.all()
            return [x.to_dict() for x in books], 200


class UserSection(Resource):
    @jwt_required()
    def get(self, section_id=None):
        if section_id :
            section = Section.query.filter_by(id=section_id).first()
            return (section.to_dict(), 200) if section else ("not found", 404)
        else : 
            sections = Section.query.all()
            return [x.to_dict() for x in sections], 200

class RequestBook(Resource):
    @jwt_required()
    def __init__(self):
        self.user_id = get_jwt_identity()
        
    def get(self, book_id):
        pass
    @jwt_required()
    def post(self, book_id):
        
        try :

            user = User.query.filter_by(id=self.user_id).first()

            if user.requested_books == 5 :
                return "can't add more", 200
            user.requested_books += 1 
            
            check = db.session.query(user_book_association).filter_by(user_id= self.user_id, book_id=book_id).first()
            if  check:
                db.session.query(user_book_association).filter_by(user_id= self.user_id, book_id=book_id).update({'status': '0'})
            else :
                db.session.execute(user_book_association.insert().values({'book_id' : book_id, 'user_id' : self.user_id }))
            return "request send",200
        except : 
            db.session.rollback()
            return "check user_id, book_id, or can't request more", 400
        finally:
            db.session.commit()

    @jwt_required()
    def delete(self,  book_id):
    

        user = User.query.filter_by(id=self.user_id).first()
        user.requested_books -= 1
        db.session.query(user_book_association).filter_by(user_id= self.user_id, book_id=book_id).update({'status':3})
        db.session.commit()

class BookFeedback(Resource):
    @jwt_required()
    def __init__(self):
        self.user_id = get_jwt_identity()
    @jwt_required()
    def get(self, book_id):
        feedback = db.session.query(user_book_association).filter_by(user_id=self.user_id, book_id=book_id).first()
        return (user_book_association_to_dict(feedback), 200) if feedback else ("not found", 404)
    @jwt_required()
    def put(self,  book_id):
        try :
            rating_parser = reqparse.RequestParser()
            rating_parser.add_argument('rating')
            rating_parser.add_argument('rating_description')
            args = rating_parser.parse_args()
            db.session.query(user_book_association).filter_by(user_id= self.user_id, book_id=book_id).update({'rating':args['rating'] , 'rating_description':args['rating_description'], 'rated_date':datetime.datetime.now()})
            return "thanks for rating", 200
        except  : 
            db.session.rollback()
            return "check userid, book_id, you should have read this book atleast once", 400
        finally : 
            db.session.commit()
    @jwt_required()
    def post(self, book_id):
        rating_parser = reqparse.RequestParser()
        rating_parser.add_argument('rating')
        rating_parser.add_argument('rating_description')
        args = rating_parser.parse_args()
        args['user_id'] = self.user_id
        args['book_id'] = book_id
        db.session.execute(user_book_association.insert().values(**args))
        db.session.commit()
        return "thanks for rating", 200
class UserBookHistory(Resource):
    @jwt_required()
    def __init__(self):
        self.user_id = get_jwt_identity()
    @jwt_required()
    def get(self):
        books = db.session.query(user_book_association).filter_by(user_id= self.user_id).all()
        print(books)
        return [user_book_association_to_dict(row) for row in books]
    

class BookStatus(Resource):
    @jwt_required()
    def __init__(self):
        self.user_id = get_jwt_identity()
    @jwt_required()
    def get(self, book_id):
        book = db.session.query(user_book_association).filter_by(user_id=self.user_id , book_id=book_id).first()
        
        return user_book_association_to_dict(book), 200
        