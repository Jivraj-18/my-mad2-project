from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import os

from database.model import db, User
from functions import create_admin
from config import Config
from register_resources import register_resources
from test_data import add_test_data

from celery.schedules import crontab
from workers import celery_init_app
from tasks import daily_reminder, monthly_report
from flask import jsonify
from tasks import generate_user_csv
from flask import send_file
import redis
from io import BytesIO

# Create Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://frontend-mad2-project.vercel.app/"}})


# Load configurations from config.py
app.config.from_object(Config)
celery_app = celery_init_app(app)

# Initialize database
db.init_app(app)

# Create database tables if they don't exist
if not os.path.exists(os.path.join(os.getcwd(), 'database', 'database.sqlite3')):
    with app.app_context():
        db.create_all()
        create_admin()
        add_test_data(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask-Restful API
api = Api(app)

# Register resources/endpoints
register_resources(api)

# Retrieve admin email within the application context
with app.app_context():
    admin = (User.query.filter_by(role=1).first()).email

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=11, minute=26, day_of_month="*"),
        daily_reminder.s(admin, 'Daily Test'),
    )
    sender.add_periodic_task(
        crontab(hour=11, minute=26, day_of_month="22"),
        monthly_report.s(admin, 'Daily Test'),
    )




@app.route('/generate_csv')
def generate_csv():
    task = generate_user_csv.delay()  # Run the task asynchronously
    return jsonify({'task_id': task.id}), 202


r = redis.Redis(host='localhost', port=6379, db=2)

@app.route('/download_csv', methods=['GET'])
def download_csv():
    # Retrieve the CSV content from Redis
    csv_content = r.get('user_data_csv')
    
    if csv_content:
        # Use BytesIO to create a file-like object
        csv_file = BytesIO(csv_content)
        csv_file.seek(0)

        # Send the CSV file as an attachment
        return send_file(
            csv_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name='user_data.csv'  # Use download_name instead of attachment_filename
        )
    else:
        return jsonify({"message": "CSV file not found. Please generate it first."}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
