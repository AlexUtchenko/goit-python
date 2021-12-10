from flask import render_template, flash, url_for, redirect
from cb_app import app, db
from flask_login import login_user, login_required, current_user, logout_user
from cb_app.forms import LoginForm, RegistrationForm, RequestForm, EditForm
from cb_app.models import User, Contact


@app.route('/', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # form = NoteForm()
    # if form.validate_on_submit():
    #     post = Note(body=form.note.data, author=current_user)
    #     db.session.add(post)
    #     db.session.commit()
    #     flash('Your post is now live!')
    #     return redirect(url_for('index'))
    # notes = Note.query.filter_by(author=current_user).all()
    return render_template("index.html")


@app.route('/index/add', methods=['GET', 'POST'])
@login_required
def add():
    form = EditForm()
    if form.validate_on_submit():
        post = Contact(name=form.name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(post)
        db.session.commit()
        flash('The record has been added!')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/index/show_all', methods=['GET'])
@login_required
def show_all():
    contacts = Contact.query.all()
    return render_template('show_all.html', contacts=contacts)

@app.route('/index/request', methods=['GET', 'POST'])
@login_required
def delete():
    form = RequestForm()
    if form.validate_on_submit():
        record_id = Contact.query.filter_by(name=form.data.data).one()
        record = Contact.query.get_or_404(record_id.id)
        db.session.delete(record)
        db.session.commit()
        flash('The record has been deleted!')
        return redirect(url_for('index'))
    return render_template('request.html', form=form)


@app.route('/index/show', methods=['GET', 'POST'])
@login_required
def show():
    form = RequestForm()
    record = None
    name = "contact name"
    if form.validate_on_submit():
        record = Contact.query.filter_by(name=form.data.data).all()
        if not record:
            record = 0
    return render_template('show.html', form=form, record=record, name=name)


@app.route('/index/search', methods=['GET', 'POST'])
@login_required
def search():
    form = RequestForm()
    contacts = None
    name = 'searching data'
    if form.validate_on_submit():
        contacts = Contact.query.filter(Contact.phone.like('%' + form.data.data + '%')).all()
        contacts.extend(Contact.query.filter(Contact.email.like('%' + form.data.data + '%')).all())
        contacts.extend(Contact.query.filter(Contact.name.like('%' + form.data.data + '%')).all())
        if not contacts:
            contacts = 0
    return render_template('show.html', form=form, record=contacts, name=name)
