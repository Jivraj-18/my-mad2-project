from database.model import User, db
from werkzeug.security import generate_password_hash
def create_admin():
    user = User(f_name="admin", password=generate_password_hash("1234"), email="admin@1.com",role=1 )
    db.session.add(user)
    db.session.commit()