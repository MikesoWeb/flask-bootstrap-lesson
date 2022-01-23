from flask import Blueprint, render_template, url_for
from flask import Markup
from flask_login import login_required, current_user

from models import Employee

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@login_required
def index():
    empl = Employee.query.limit(5).all()
    spin = Markup(
        """<div class="spinner-border spinner-border-sm" role="status">
         <span class="visually-hidden">Loading...</span>
        </div>""")
    image_file = url_for('static',
                         filename=f'profile_pics' + '/employees_pics/' + current_user.email +
                                  current_user.image_file)
    return render_template('main/index.html', empl=empl, image_file=image_file, spin=spin)


