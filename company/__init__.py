
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from company.employee.utils import random_avatar

db = SQLAlchemy()
bcrypt = Bcrypt()
bootstrap = Bootstrap5()


login_manager = LoginManager()
login_manager.login_view = 'employee.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Авторизуйтесь, чтобы попасть в панель управления'


def create_user():
    from models import Employee

    users = {
        1: {
            'first_name': 'Михаил', 'last_name': 'Терехов',
            'email': 'admin@gmail.com', 'password': '12345', 'position': 'CEO'},
        2: {
            'first_name': 'Василий', 'last_name': 'Пупкин',
            'email': 'vas_pupkin@gmail.com', 'password': '23452', 'position': 'TeamLead'},
        3: {
            'first_name': 'Василий', 'last_name': 'Стрельцов',
            'email': 'vas_strel@gmail.com', 'password': '554756', 'position': 'TechLead'},
        4: {
            'first_name': 'Мария', 'last_name': 'Перепелкина',
            'email': 'masha_perepelkina@gmail.com', 'password': 'пррп676', 'position': 'HR'},
        5: {
            'first_name': 'Александр', 'last_name': 'Пуговкин',
            'email': 'pugovkin@gmail.com', 'password': 'dfhtgf56756', 'position': 'Junior'}
    }

    for i in users.values():
        user = Employee(first_name=i['first_name'], last_name=i['last_name'], email=i['email'],
                        password=bcrypt.generate_password_hash(i['password']), position=i['position'])

        if not Employee.query.filter_by(email=user.email).first():
            db.session.add(user)
            user.image_file = random_avatar(user.email)
            db.session.commit()
        else:
            return f'User c адресом {user.email} уже существует!'




def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from company.main.routes import main
    from company.employee.routes import employee
    app.register_blueprint(main)
    app.register_blueprint(employee)

    return app