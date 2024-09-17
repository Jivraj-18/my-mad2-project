from flask import session, request, jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required
from database.model import *

class BookSearch(Resource):
    def get(self):
        query = request.args.get('query')
        filter_column = request.args.get('filter', 'name')  # Default to 'name' if no filter is provided

        # Define the columns to search
        columns = {
            'name': Book.name,
            'description': Book.description,
            'author': Book.author,
            'section_name': Section.name
        }

        # Validate the filter_column
        if filter_column not in columns:
            return jsonify({'error': 'Invalid filter column'}), 400

        if query:
            # Build the query dynamically based on the filter_column
            search_query = columns[filter_column].ilike(f"%{query}%")
            
            if filter_column == 'section_name':
                # Special case for searching section name
                search_results = Book.query.join(Book.sections).filter(search_query).all()
            else:
                # Standard case for searching book fields
                search_results = Book.query.join(Book.sections).filter(
                    search_query
                ).all()

            # Convert search results to JSON
            search_results_json = [
                {
                    'id': book.id,
                    'name': book.name,
                    'description': book.description,
                    'author': book.author,
                    'rating': book.rating
                }
                for book in search_results
            ]
            return jsonify(search_results_json)
        else:
            return jsonify([])



class SectionSearch(Resource):
    def get(self):
        query = request.args.get('query')

        if query:
            # Perform search query
            search_results = Section.query.filter(
                (Section.name.ilike(f"%{query}%"))
            ).all()
            # Convert search results to JSON
            search_results_json = [
                {
                    'id': section.id,
                    'name': section.name,
                    'description': section.description,
                }
                for section in search_results
            ]
            return jsonify(search_results_json)
        else:
            return jsonify([])

