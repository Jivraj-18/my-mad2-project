from flask import session, request
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from database.model import *
import os
from resources.functions import extract_first_page_as_png, get_num_pages,convert_to_png


class BookApi(Resource):
    # @jwt_required()
    def get(self, book_id=None):

        if book_id :
            book = Book.query.filter_by(id=book_id).first()
            return (book.to_dict(), 200) if book else ("bad request", 400)
        else : 
            books = Book.query.all()
            return [x.to_dict() for x in books], 200 
    
    # @jwt_required()
    def post(self):
        # try :
        # print(request.files.get('file'))
        new_book = Book(name=(request.form).get('name'), description = (request.form).get('description'), author=(request.form).get('author'))
        db.session.add(new_book)
        db.session.flush()
        request.files.get('book_pdf').save(os.path.join(os.getcwd(), 'static','pdfs',str(new_book.id)+'.pdf'))
        book_path = os.path.join(os.getcwd(),'static','pdfs',str(new_book.id)+'.pdf')
        extract_first_page_as_png(book_path,os.path.join(os.getcwd(),'static','images','book',str(new_book.id)+'.png'))
        
        # new_book.page_count = get_num_pages(book_path)
        
        db.session.commit()
        # return True,200
        return new_book.to_dict(),200
        # except :
        #     return "bad request",400
    @jwt_required()
    def put(self, book_id):
        try : 
            book = Book.query.filter_by(id=book_id).first()

        
            book.name = (request.form).get('name')
            book.description = (request.form).get('description')
            book.author = (request.form).get('author')
            
            if (request.form).get('change_pdf') == '1' : # change_pdf == '1' means librarian wants to change pdf file               
                request.files.get('book_pdf').save(os.path.join(os.getcwd(), 'static','pdfs',str(book.id)+'.pdf'))
                book_path = os.path.join(os.getcwd(),'static','pdfs',str(book.id)+'.pdf')
                extract_first_page_as_png(book_path,os.path.join(os.getcwd(),'static','images','book',str(book.id)+'.png'))
                book.page_count = get_num_pages(book_path)
            db.session.commit()
            return book.to_dict(), 200
        except:
            return 'check book id', 400
    @jwt_required()
    def delete(self, book_id):
        try : 
            book = Book.query.filter_by(id=book_id).first()
            try : 

                os.remove(os.path.join(os.getcwd(),'static','pdfs',str(book_id)+'.pdf'))
                os.remove(os.path.join(os.getcwd(),'static','images','book',str(book_id)+'.png'))
            except :
                pass
            db.session.delete(book)
            db.session.commit()
            return "successfully deleted",200
        except : 
            return 'check book id', 404
        



class SectionApi(Resource):
    @jwt_required()
    def get(self, section_id=None):
        if section_id : 
            section = Section.query.filter_by(id=section_id).first()
            return (section.to_dict(), 200) if section else ("not found", 404)
        return [x.to_dict() for x in Section.query.all()]

    @jwt_required()
    def post(self):
        try : 
            new_section = Section(name=(request.form).get('name'),description=(request.form).get('description'))
            db.session.add(new_section)
            db.session.flush()
            file_uploaded = request.files.get('section_image')
            if (file_uploaded.filename).split('.')[-1] != 'png':
                convert_to_png(file_uploaded).save(os.path.join(os.getcwd(), 'static','images','section',str(new_section.id)+'.png'))
            else : 
                file_uploaded.save(os.path.join(os.getcwd(), 'static','images','section',str(new_section.id)+'.png'))
            # convert_to_png(request.files.get('section_image')).save(os.path.join(os.getcwd(), 'static','images','section',str(new_section.id)+'.png'))
            print(new_section.to_dict())
            return new_section.to_dict(),200
        except : 
            db.session.rollback()
            return "bad request", 400
        finally :
            db.session.commit()
    @jwt_required()
    def put(self, section_id):
        try : 
            section = Section.query.filter_by(id=section_id).first()
        
            section.name = (request.form).get('name')
            section.description = (request.form).get('description')
            
            file_uploaded = request.files.get('section_image')
            if (file_uploaded.filename).split('.')[-1] != 'png':
                convert_to_png(file_uploaded).save(os.path.join(os.getcwd(), 'static','images','section',str(section.id)+'.png'))
            else : 
                file_uploaded.save(os.path.join(os.getcwd(), 'static','images','section',str(section.id)+'.png'))
            
            return section.to_dict(), 200
        except : 
            db.session.rollback()
            return "check section id", 404
        finally :
            db.session.commit()
    
    @jwt_required()
    def delete(self, section_id):
        try : 
            section = Section.query.filter_by(id=section_id).first()
        
            db.session.delete(section)
            
            return "done", 200
        except  : 
            db.session.rollback()
            return "check section id", 404
        finally : 
            db.session.commit()

class BookSectionApi(Resource):
    @jwt_required()
    def get(self, section_id):

        section = Section.query.filter_by(id=section_id).first()
        
        return ([ x.to_dict() for x in (section.books)],200) if section else ("check section id", 400)
        
    @jwt_required()
    def post(self,section_id, book_id):
    
        try :
            section = Section.query.filter_by(id=section_id).first()
            book = Book.query.filter_by(id=book_id).first()
            section.books.append(book)
            
            return "book added to section",200
        except : 
            db.session.rollback()
            return "check section id, book id , book already exists", 400
        finally :
            db.session.commit()
    @jwt_required()
    def delete(self,section_id, book_id):
        try :
            section = Section.query.filter_by(id=section_id).first()
            book = Book.query.filter_by(id=book_id).first()
            section.books.remove(book)
            
            return "deleted successfully",200
        except : 
            db.session.rollback()
            return "check book id , section id ", 400
        finally : 
            db.session.commit()

class BookIssue(Resource):
    @jwt_required()
    def get(self,user_id=None):
        if user_id == None: 
            query = db.session.query(user_book_association).filter_by()
        else :
            query = db.session.query(user_book_association).filter_by(user_id= user_id)
        rows =  query.all()
        return  [ user_book_association_to_dict(row) for row in rows ] 
    
    @jwt_required()
    def put(self,user_id, book_id):
        try  :
            status_parser = reqparse.RequestParser()
            status_parser.add_argument('status')
            if status_parser.parse_args()['status'] == '1':
                db.session.query(user_book_association).filter_by(user_id= user_id).update({"status":status_parser.parse_args()['status'],"request_expiry_date":datetime.datetime.now()+datetime.timedelta(days=7)})

            elif status_parser.parse_args()['status'] in {'4','2'}: 
                updates = {"status":status_parser.parse_args()['status'],"request_expiry_date":datetime.datetime.now()}
                query = db.session.query(user_book_association).filter_by(user_id= user_id)
                query.update(updates)
                
            return "updated succcessfully", 200
        except :
            db.session.rollback()
            return "check user_id, book_id, status", 400
        finally : 
            db.session.commit()
    