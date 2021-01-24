from app import journal_app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, DeleteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime




@journal_app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    current_hour = datetime.now().hour

    return render_template('index.html', title='Journal/Poem App', current_hour=current_hour)

@journal_app.route('/', methods=['GET', 'POST'])
@journal_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():



        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.username.data).first()
        #If the username and email do not exist
        if user is None and email is None:
            flash('Invalid username or email')
            return redirect(url_for('login'))
        #If user exists but password is wrong
        elif user is not None and not user.check_password(form.password.data):
            flash('Wrong password')
            return redirect(url_for('login'))
        #If email id exists but password is wrong
        elif email is not None and not email.check_password(form.password.data):
            flash('Wrong password')
            return redirect(url_for('login'))
        #If username is entered and it is valid
        if user is not None:
            login_user(user, remember=form.remember_me.data)
        #If email is entered and it is valid
        elif email is not None:
            login_user(email, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@journal_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@journal_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@journal_app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@journal_app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@journal_app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Profile updated with new changes.')
        db.session.commit()
        return redirect(url_for('edit_profile'))


    return render_template('edit_profile.html', title='Edit Profile', form=form)

@journal_app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Journal posted')
    user = {'username' : 'Isha'}
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc())

    return render_template('journal.html', form=form, posts=posts)


@journal_app.route('/new_entry', methods=['GET', 'POST'])
@login_required
def new_entry():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Journal entry recorded")
        return redirect(url_for('journal'))
    return render_template('new_entry.html', form=form)

@journal_app.route('/past_entry/<int:record_id>/', methods=['GET', 'POST'])
@login_required
def past_entry(record_id):
    record = Post.query.get(int(record_id))
    form = DeleteForm()
    #Proceed with deleting the post if delete button pressed
    if form.is_submitted() or request.method == 'POST':
        db.session.delete(record)
        db.session.commit()
        flash("Journal entry deleted")
        return redirect(url_for('journal'))

    if record is not None:
        return render_template('post.html', record=record, form=form)
    else:
        return render_template('404.html')
