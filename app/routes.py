from app import app
from app.forms import LoginForm
from app.models import User
from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, current_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(''))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for(''))

    return render_template('login.html', form=form)