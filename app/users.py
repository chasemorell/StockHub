from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html',title='Sign In', form=form)

#TODO THIS METHOD IS A WORK IN PROGRESS
@bp.route('/loginRedirect/<path:text>', methods=['GET', 'POST'])
def loginRedirect(text):
    print("redirect login!")
    reasonForRedirect = text
    print(reasonForRedirect)
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', reasonForRedirect = reasonForRedirect,title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/transferSubmit', methods=['GET', 'POST'])
def submit_transfer():
    if current_user.is_authenticated:
        type = int(request.form.get('acctype'))
        id = current_user.id
        amount = float(request.form.get('amntinfo'))

        if type == 1: #deposit
            User.deposit(id, amount)
        elif type == 2: #withdraw 
            withdraw_amount = min(amount, current_user.get_available_balance(current_user.id))
            User.withdraw(id, withdraw_amount)
        else:
            print("Invalid Code")
        
        
        return render_template('transferSubmit.html')

    return redirect(url_for('users.login', reasonForRedirect="You must login to write an article."))

@bp.route('/transferMoney', methods=['GET', 'POST'])
def transfer():
    # Get all stocks
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to transfer money."))

    return render_template("transfer_money.html", 
                            available_balance=current_user.get_available_balance(current_user.id), 
                            current_user=current_user, 
                            email=current_user.email) 

@bp.route('/portfolio', methods=['GET', 'POST'])
def portfolio_login():
    # Get all stocks
    if not current_user.is_authenticated:
        return redirect(url_for('users.login', reasonForRedirect="You must login to see your portfolio."))

    return render_template("portfolio.html") 