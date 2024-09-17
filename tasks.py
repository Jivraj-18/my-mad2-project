
from celery import shared_task

from mail_service import send_message
# from .models import User, Role
from jinja2 import Template
from database.model import User, Book, db, user_book_association_to_dict,user_book_association
from sqlalchemy import func


@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.filter_by(role = 0).all()
    admin = User.query.filter_by(role = 1).first()

    for user in users:
        with open('daily.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,
                            template.render(username=user.f_name, adminname=admin.email))
    return "OK"

# from models import Book_issue
@shared_task(ignore_result=True)
def monthly_report(to, subject):
    users = User.query.filter_by(role=0).all()
    admin = User.query.filter_by(role = 1).first()
    for user in users:

        rows = db.session.query(user_book_association).filter_by(user_id= user.id).all()
        json_data = [user_book_association_to_dict(row) for row in rows]

        send_message(user.email, subject, generate_html_report(json_data=json_data, admin=admin))




def generate_html_report(json_data,admin):
    # Start the HTML structure
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Monthly Book Report</h1>
        
        <table>
            <tr>
                <th>User Email</th>
                <th>Book Name</th>
                <th>Status</th>
                <th>Rating</th>
                <th>Rating Description</th>
                <th>Request Date</th>
                <th>Request Expiry Date</th>
                <th>Previously Read</th>
            </tr>
    """

    # Add data rows to the HTML
    for item in json_data:
        book_details = item['book_details']
        html_content += f"""
        <tr>
            <td>{item['user_details']['email']}</td>
            <td>{book_details['name']}</td>
            <td>{get_status_text(item['status'])}</td>
            <td>{item['rating'] if item['rating'] else 'N/A'}</td>
            <td>{item['rating_description'] if item['rating_description'] else 'N/A'}</td>
            <td>{item['request_date']}</td>
            <td>{item['request_expiry_date'] if item['request_expiry_date'] else 'N/A'}</td>
            <td>{"Yes" if item['previously_read'] else "No"}</td>
        </tr>
        """

    # Close the HTML structure
    html_content += f"""
        </table>
        <p>Happy reading!</p>
        <p>Best regards,</p>
        <p>{admin.email}</p>
    </body>
    </html>
    """

    return html_content

def get_status_text(status_code):
    status_mapping = {
        0: 'Pending',
        1: 'Accepted',
        2: 'Rejected',
        3: 'Returned',
        4: 'Revoked'
    }
    return status_mapping.get(status_code, 'Unknown')



import csv
import redis
from io import StringIO
from celery import shared_task
from database.model import User

# Set up Redis for temporary storage
r = redis.Redis(host='localhost', port=6379, db=2)

@shared_task()
def generate_user_csv():
    # Query your database for user details
    users = User.query.all()

    # Prepare CSV data in-memory
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(['user_id', 'name', 'email'])  # Add your relevant fields here

    for user in users:
        writer.writerow([user.id, user.f_name, user.email])

    # Store CSV content in Redis
    r.set('user_data_csv', csv_file.getvalue())
    return "CSV generated and stored in Redis"