from datetime import datetime
from werkzeug.security import generate_password_hash
def add_users(app, db, User):
    
    users_data = [
        {"f_name": "John", "l_name": "Doe", "email": "john.doe@example.com", "password": generate_password_hash("password1"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Jane", "l_name": "Smith", "email": "jane.smith@example.com", "password": generate_password_hash("password2"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Alice", "l_name": "Johnson", "email": "alice.johnson@example.com", "password": generate_password_hash("password3"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Bob", "l_name": "Brown", "email": "bob.brown@example.com", "password": generate_password_hash("password4"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Emily", "l_name": "Wilson", "email": "emily.wilson@example.com", "password": generate_password_hash("password5"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Michael", "l_name": "Taylor", "email": "michael.taylor@example.com", "password": generate_password_hash("password6"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Sophia", "l_name": "Martinez", "email": "sophia.martinez@example.com", "password": generate_password_hash("password7"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "David", "l_name": "Anderson", "email": "david.anderson@example.com", "password": generate_password_hash("password8"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "Olivia", "l_name": "Garcia", "email": "olivia.garcia@example.com", "password": generate_password_hash("password9"), "role": 1, "last_visited": datetime.now(), "verified": True},
        {"f_name": "William", "l_name": "Rodriguez", "email": "william.rodriguez@example.com", "password": generate_password_hash("password10"), "role": 1, "last_visited": datetime.now(), "verified": True}
    ]

    for user_data in users_data:
      
        db.session.add(User(**user_data))

