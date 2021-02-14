from sqlite3 import IntegrityError

from flask import Blueprint, render_template, flash, redirect, url_for, request

from my_app import db
from my_app.auth.forms import SignupForm, LoginForm
from my_app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.firstname} {user.lastname}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.email.data
        flash(f"You are logged in as {name}.")
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form=form)
