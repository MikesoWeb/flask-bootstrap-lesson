from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask import Markup

from models import Employee
from company import db, bcrypt
from company.employee.forms import LoginForm

employee = Blueprint('employee', __name__, template_folder='templates')


@employee.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('employee.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вы вошли как сотрудник {current_user.first_name} {current_user.last_name}', 'info')
            return redirect(next_page) if next_page else redirect(url_for('employee.dashboard'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте электронную почту или пароль', 'danger')
    return render_template('employee/login.html', form=form, title='Логин', legend='Войти')


@employee.route('/dashboard')
@login_required
def dashboard():
    empl = Employee.query.all()
    spin = Markup(
        """<div class="spinner-border spinner-border-sm" role="status">
         <span class="visually-hidden">Loading...</span>
        </div>""")
    image_file = url_for('static',
                         filename=f'profile_pics' + '/employees_pics/' + current_user.email +
                                  current_user.image_file)
    return render_template('employee/employees.html', empl=empl, image_file=image_file, spin=spin)


@employee.route('/employee/<string:email_str>')
@login_required
def account(email_str):
    entry = Employee.query.filter_by(email=email_str).first()
    return render_template('employee/single_user.html', entry=entry)


@employee.route('/employee/action/<string:email_str>')
@login_required
def action_user(email_str):
    entry_action = Employee.query.filter_by(email=email_str).first()
    return render_template('employee/action_user.html', entry_action=entry_action)


@employee.route('/employee/edit/<string:email_str>')
@login_required
def edit_user(email_str):
    entry_edit = Employee.query.filter_by(email=email_str).first()
    return render_template('employee/edit_info.html', entry_edit=entry_edit)


@employee.route('/employee/settings/<string:email_str>')
@login_required
def settings_user(email_str):
    entry_settings = Employee.query.filter_by(email=email_str).first()
    return render_template('employee/settings_user.html', entry_settings=entry_settings)


# https://pypi.org/project/Flask-Seeder/
@employee.route('/log_out')
def log_out():
    current_user.last_seen = datetime.now()
    db.session.commit()
    logout_user()
    return redirect(url_for('employee.login'))
