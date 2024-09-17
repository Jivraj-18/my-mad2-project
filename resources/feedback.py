from flask import session, request
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.model import *

class Feedback(Resource):
    @jwt_required()
    def get(self, book_id):
        books = db.session.query(user_book_association).filter_by( book_id=book_id).all()
        return [user_book_association_to_dict(book) for book in (books or [])]
    