from datetime import datetime
from flask import render_template, flash, redirect, g, session, url_for
from pyrebase import pyrebase
from forms import LoginForm, EditForm, SearchForm, PostForm
from flask_login import login_required, logout_user, current_user, login_user
from app import app, db, lm, babel
from models import User, Post


firebase = pyrebase.initialize_app(app.config['FIREBASE_CONFIG'])
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    created_at=datetime.utcnow(),
                    created_by=g.user.id,
                    updated_at=datetime.utcnow(),
                    updated_by=g.user.id,
                    user_id=g.user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    print '=========='
    user = g.user
    return render_template('index.html', title='Home', user=user, form=form, posts=user.followed_posts())

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
    return render_template('user.html', user=user, posts=user.posts)

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

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.filter(Post.body.like('%' + query + '%')).all()
    return render_template('search_results.html', query=query, results=results)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user==g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))

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
        g.search_form = SearchForm()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.hml'), 500

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())
