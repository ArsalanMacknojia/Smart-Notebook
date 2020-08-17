import os
import uuid
import ctypes
import logging
from PIL import Image
from flask_mail import Message
from sqlalchemy import or_, and_
from numpy.ctypeslib import ndpointer
from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request, jsonify

from smart_notebook import app, db, bcrypt, mail
from smart_notebook.models import User, Note
from smart_notebook.forms import LoginForm, SignUpForm, NoteForm, UpdateNoteForm, FibonacciForm, RequestResetForm, \
    ResetPasswordForm, AccountUpdateForm, SearchForm, QuadraticForm

LOGGER = logging.getLogger(__name__)


# -------------------------------------------------Login/Logout---------------------------------------------------------

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Incorrect email or password. Please try again!', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))


# ----------------------------------------------------SignUp------------------------------------------------------------

@app.route("/signup/", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, phone_number=form.phone_number.data,
                    postal_code=form.postal_code.data.replace(" ", "").upper(),
                    password=hash_pw)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Account created!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Register', form=form)


# ---------------------------------------------------Forgot Pass--------------------------------------------------------

def send_reset_email(user):
    token = user.get_reset_token()
    email = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    email.body = f''' 
    Visit the following link to reset your Smart Notebook password: {url_for('reset_token', token=token, _external=True)}
    If you did not make this request, please ignore this email.
    '''
    mail.send(email)


@app.route("/reset_password/", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with instruction has been sent to your email', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>/", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash("Token is invalid or expired.", 'danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pw
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# -----------------------------------------------------Home-------------------------------------------------------------


@app.route("/", methods=['GET', 'POST'])
@app.route("/home/", methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = SearchForm()
    if form.validate_on_submit():
        search_str = form.search_content.data
        notes = db.session.query(Note).filter(
            and_(Note.author == current_user, or_(Note.title.ilike(search_str), Note.content.ilike(search_str)))).all()
        if not notes:
            flash("No results found!", "danger")
            return render_template('home.html', notes=[], form=form)
        flash("Search Found!", "success")
        return render_template('home.html', notes=notes, form=form)

    notes = Note.query.filter_by(author=current_user).all()
    return render_template('home.html', notes=notes, form=form)


# ----------------------------------------------------About-------------------------------------------------------------

@app.route("/about/")
def about():
    return render_template('about.html')


# ----------------------------------------------------Notes-------------------------------------------------------------

# Get specific post
@app.route("/note/<int:note_id>/", methods=['GET'])
@login_required
def note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('note.html', note=note)


# Create new note
@app.route("/note/new/", methods=['GET', 'POST'])
@login_required
def new_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(author=current_user, title=form.title.data, content=form.content.data)
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_note.html', form=form, legend='New Note')


# Update note
@app.route("/note/<int:note_id>/update/", methods=['GET', 'POST'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = UpdateNoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('note', note_id=note.id))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('create_note.html', form=form, legend='Update Note')


# Delete note
@app.route("/note/<int:note_id>/delete/", methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Your note has been deleted!', 'success')
    return redirect(url_for('home'))


# -----------------------------------------------------Account----------------------------------------------------------

# Get Account
@app.route("/account/", methods=['GET'])
@login_required
def get_account():
    # user = User.query.filter_by(id=current_user.id).first()
    # return render_template('account.html', account=user), 200
    return render_template('account.html')


def save_image(picture):
    picture_name = uuid.uuid4().hex + '.jpg'
    picture_path = os.path.join(app.root_path, 'static', 'user_images', picture_name)
    reduced_size = (125, 125)
    user_image = Image.open(picture)
    user_image.thumbnail(reduced_size)
    user_image.save(picture_path)
    return picture_name


# Edit Account
@app.route("/account/edit/", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            try:
                picture_name = save_image(form.picture.data)
                current_user.user_image = picture_name
            except Exception as e:
                LOGGER.error("Invalid image extension: ", e)
                flash("Invalid image extension! ", "danger")
                return redirect(url_for('edit_account'))
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.postal_code = form.postal_code.data.upper()
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('edit_account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.postal_code.data = current_user.postal_code
    user_image = url_for('static', filename='user_images/' + current_user.user_image)
    return render_template('edit_account.html', title='Edit Account', user_image=user_image, form=form)


# ------------------------------------------------Autocomplete----------------------------------------------------------

@app.route('/autocomplete/', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    notes = db.session.query(Note).filter(or_(Note.title.ilike(search), Note.content.ilike(search))).all()
    results = [note.as_dict() for note in notes]
    return jsonify(matching_results=results)


# ------------------------------------------------Catch All-------------------------------------------------------------

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('error.html')


# ------------------------------------------------Arithmetic------------------------------------------------------------

# Helper Functions
def c_fib(start, length):
    path = "{},smart_notebook,c_arithmetic,arithmetic.so".format(os.getcwd())
    path = path.split(",")
    c_file_path = os.path.join(*path)
    c_arithmetic = ctypes.cdll.LoadLibrary(c_file_path)

    fib_sequence = []
    for x in range(start, start + length):
        fib_sequence.append(c_arithmetic.fib(ctypes.c_int(x)))
    return fib_sequence


def c_quad_roots(a, b, c):
    path = "{},smart_notebook,c_arithmetic,arithmetic.so".format(os.getcwd())
    path = path.split(",")
    c_file_path = os.path.join(*path)
    c_arithmetic = ctypes.cdll.LoadLibrary(c_file_path)
    c_arithmetic.quadRoots.restype = ndpointer(dtype=ctypes.c_float, shape=(2,))

    return c_arithmetic.quadRoots(ctypes.c_int(a), ctypes.c_int(b), ctypes.c_int(c))


# Default Arithmetic
@app.route("/arithmetic/", methods=['GET', 'POST'])
def arithmetic():
    form = FibonacciForm()
    return render_template('arithmetic.html', form=form, legend='Fibonacci', result=None)


# Fibonacci Sequence
@app.route("/arithmetic/fibonacci/", methods=['GET', 'POST'])
def arithmetic_fibonacci():
    form = FibonacciForm()
    if form.validate_on_submit():
        start = form.start.data
        length = form.range.data
        result = c_fib(start, length)
        return render_template('arithmetic.html', form=form, legend='Fibonacci', result=result)
    return render_template('arithmetic.html', form=form, legend='Fibonacci', result=None)


# Quadratic Sequence
@app.route("/arithmetic/quadratic/", methods=['GET', 'POST'])
def arithmetic_quadratic():
    form = QuadraticForm()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        c = form.c.data
        result = c_quad_roots(a, b, c)
        return render_template('arithmetic.html', form=form, legend='Quadratic', result=result)
    return render_template('arithmetic.html', form=form, legend='Quadratic', result=None)
