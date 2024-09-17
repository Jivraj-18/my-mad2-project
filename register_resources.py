from resources.auth_api import SignupApi, LoginApi
from resources.librarian_api import *
from resources.user_api import *
from resources.search_api import *
from resources.feedback import *
def register_resources(api):
    # Add resources/endpoints to the API
    api.add_resource(SignupApi, "/api/signup/")
    api.add_resource(LoginApi, "/api/signin/")
    
    api.add_resource(UserIssuedBook,"/api/user/books/issued")
    api.add_resource(UserBookApi, "/api/user/book/<int:book_id>", "/api/user/books")
    api.add_resource(UserSection, "/api/user/sections","/api/user/section/<int:section_id>")
    api.add_resource(BookSectionApi,"/api/user/section/<int:section_id>/books","/api/librarian/section/<int:section_id>/books","/api/librarian/section/<int:section_id>/book/<int:book_id>")
    api.add_resource(RequestBook, "/api/user/book/<int:book_id>/request","/api/librarian/section/<int:section_id>/book/<int:book_id>")
    api.add_resource(BookFeedback, "/api/user/book/<int:book_id>/feedback")
    api.add_resource(UserBookHistory, "/api/user/history/book")
    api.add_resource(BookStatus, "/api/user/status/<int:book_id>")
    api.add_resource(CanRequestBook, "/api/user/can_request")
    api.add_resource(Feedback, '/api/book/<int:book_id>/feedbacks')
    api.add_resource(SectionApi,"/api/librarian/section","/api/librarian/section/<int:section_id>")
    api.add_resource(BookApi,"/api/librarian/book","/api/librarian/book/<int:book_id>")
    api.add_resource(BookIssue, "/api/librarian/book/<int:book_id>/issue/<int:user_id>", "/api/librarian/book/issue" )

    api.add_resource(SectionSearch, "/api/search/section")
    api.add_resource(BookSearch, "/api/search/book")

