from flask import session, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token
from database.model import *
import datetime
class SignupApi(Resource):
    def get(self):
        return "token is valid", 200
    def post(self):
        signup_parser = reqparse.RequestParser()
        
        signup_parser.add_argument('password')
        signup_parser.add_argument('email')
        arguments = signup_parser.parse_args()
        
        password = arguments.get('password', None)
        email = arguments.get('email', None)
        role = 1

        
        if (email is not None ):
            user = db.session.query(User).filter(User.email==email).first()
            if user is not None : 
                return "user exists", 409
            
            add_new_user = User(email = email, password=generate_password_hash(password),  role=role)
            db.session.add(add_new_user)
            db.session.commit()

            return "profile created successfully", 201
        else :
            return "User name or email can't be blank",400
        
class LoginApi(Resource):
    def post(self ):
        
        login_parser = reqparse.RequestParser()
        login_parser.add_argument('password')
        login_parser.add_argument('email')
        arguments = login_parser.parse_args()
        print(arguments)
        password = arguments.get('password', None)
        email = arguments.get('email', None)
        
        if (email ) and (password ): 
            
            user = db.session.query(User).filter( User.email==email).first()
            print(check_password_hash(user.password, password))
            if user and check_password_hash(user.password, password) : 
                access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=240) )
                return {"user":user.to_dict(), "access_token":access_token}, 200
            else :
                return "user does not exist", 404
            # return "Login failed, check email or password", 401
        else :
            return "email can't be blank",400
        
