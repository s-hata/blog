from datetime import datetime
from flask import render_template, flash, redirect, g, session, url_for
from pyrebase import pyrebase
from forms import LoginForm, EditForm
from flask_login import login_required, logout_user, current_user, login_user
from app import app, db, lm
from models import User

firebase = pyrebase.initialize_app(app.config['FIREBASE_CONFIG'])
auth = firebase.auth()

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        },
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        flash('Login request for User ID="%s", remember_me=%s' %
            (form.email.data, str(form.remember_me.data)))
        return signin(form.email.data, form.password.data, form.remember_me.data)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signin')
def authentication():
    return render_template('signin.html', title='Sign In')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

def signin(email, password, remember_me):
    user = auth.sign_in_with_email_and_password(email, password)
    userinfo = User.query.filter_by(email=user['email']).first()
    if userinfo is None:
        if user['displayName'] is None or user['displayName'] == "":
            nickname = user['email'].split('@')[0]
        userinfo = User(nickname=nickname, email=user['email'])
        db.session.add(userinfo)
        db.session.commit()
    login_user(userinfo , remember = remember_me)
    return redirect('/index')

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.hml'), 500
