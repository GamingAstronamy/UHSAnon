from flask_login.utils import logout_user
from app import app
from app.forms import LoginForm
from app.models import User, Post
from flask import render_template, redirect, url_for, send_from_directory
from flask_login import login_required, login_user, current_user

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', posts=Post.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post')
def post():
    return render_template('post_template.html', username=Post.query.get(1).get_username(), timestamp=Post.query.get(1).timestamp.strftime('%A %m/%d/%Y %I:%M %p'), content=Post.query.get(1).content)