import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from corkandink import app, db, bcrypt
from corkandink.forms import RegistrationForm, LoginForm, UpdateAccountForm, WineForm
from corkandink.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

wines = [
    {
        'name': 'Campo Viejo',
        'region': 'Rioja',
        'grape': 'Tempranillo',
        'country': 'Spain',
        'type': 'red',
        'picture': 'Wine Bottle',
        'rating': '4 out of 5 grapes',
        'cost': '$14',
        'wherebuy': 'Loblaws',
        'wheredrink': 'home',
        'date': '07/10/2020'
    },
    {
        'name': 'Campo Viejo',
        'region': 'Rioja',
        'grape': 'Tempranillo',
        'country': 'Spain',
        'type': 'red',
        'picture': 'Wine Bottle',
        'rating': '4 out of 5 grapes',
        'cost': '$14',
        'wherebuy': 'Loblaws',
        'wheredrink': 'home',
        'date': '07/10/2020'
    }
]


@app.route('/')
@app.route('/home')
@app.route('/homepage')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', wines=wines)
    else:
        return redirect(url_for('register.html'))
    return render_template('home.html', wines=wines)

@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, you can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed!, please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    prev_picture = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
    if os.path.exists(prev_picture) and os.path.basename(prev_picture) != 'default.jpg':
        os.remove(prev_picture)

    return picture_fn



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/wine/new', methods=['GET', 'POST'])
@login_required
def new_wine():
    form = WineForm()
    if form.validate_on_submit():
        flash('Wine added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_wine.html', title='New Wine', form=form)