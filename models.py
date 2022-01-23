from flask_login import UserMixin
from company import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    image_file = db.Column(db.String(200), nullable=False, default='default.jpg')
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), index=True)
    last_seen = db.Column(db.DateTime)
    date = db.Column(db.DateTime)
    position = db.Column(db.String(120), nullable=False)
    payment = db.Column(db.String(120))


class Employee(Staff):
    def __init__(self, *args, **kwargs):
        super(Staff, self).__init__(*args, **kwargs)

        self.boss = db.relationship('Boss', backref='staff', lazy=True)

    def __repr__(self):
        return f'Employee({self.id}, {self.first_name}, {self.last_name})'


