from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import AuthService
from app import db
from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.csrf import generate_csrf

auth_bp = Blueprint('auth', __name__)


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')


class RegisterForm(Form):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                      validators=[DataRequired(), EqualTo('password')])
    
    def validate_email(self, field):
        from models.user import User
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('An account with this email already exists.')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user, error = AuthService.authenticate_user(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        flash(error, 'error')
    
    return render_template('auth/login.html', form=form, csrf_token=generate_csrf())


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegisterForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user, error = AuthService.register_user(
            form.email.data,
            form.password.data,
            form.first_name.data,
            form.last_name.data
        )
        if user:
            login_user(user)
            flash(f'Welcome to ScriptFlow, {user.first_name}!', 'success')
            return redirect(url_for('dashboard.index'))
        flash(error, 'error')
    
    return render_template('auth/register.html', form=form, csrf_token=generate_csrf())


@auth_bp.route('/guest')
def guest():
    from flask_login import login_user
    user = AuthService.create_guest_user()
    login_user(user)
    flash('Welcome to ScriptFlow! You can explore the app without an account.', 'info')
    return redirect(url_for('dashboard.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    AuthService.logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
