# from database.model import Book
# from sqlalchemy import event
# import os 
# from resources.functions import extract_first_page_as_png
# def on_book_insert(mapper, connection, target):
#         # Your function logic here
# #     book_path = os.path.join(os.getcwd(),'static','pdfs',str(target.id)+'.pdf')
# #     print(book_path)
# #     print(os.path.join(os.getcwd(),'static','images','book',str(target.id)+'.png'))
# #     print(extract_first_page_as_png(book_path,os.path.join(os.getcwd(),'static','images','book',str(target.id)+'.png')))
#     print(f"Model {target.__class__.__name__} with id {target.id} has been changed.")

#         # Add event listener to YourModel for 'after_update', 'after_insert', and 'after_delete' events
# # event.listen(Book, 'after_update', on_book_insert)

#         # event.listen(Book, 'after_delete', on_model_change)
# event.listen(Book, 'before_insert', on_book_insert)