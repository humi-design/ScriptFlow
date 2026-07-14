from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import AuthService
from app import db
from flask_wtf.csrf import generate_csrf

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', 'off') == 'on'
        
        user, error = AuthService.authenticate_user(email, password)
        if user:
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        flash(error or 'Login failed', 'error')
    
    return render_template('auth/login.html', csrf_token=generate_csrf())


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        if not all([email, password, first_name, last_name]):
            flash('All fields are required.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', 'error')
        else:
            user, error = AuthService.register_user(email, password, first_name, last_name)
            if user:
                login_user(user)
                flash(f'Welcome to ScriptFlow, {user.first_name}!', 'success')
                return redirect(url_for('dashboard.index'))
            flash(error or 'Registration failed', 'error')
    
    return render_template('auth/register.html', csrf_token=generate_csrf())


@auth_bp.route('/guest')
def guest():
    user = AuthService.create_guest_user()
    login_user(user)
    flash('Welcome to ScriptFlow! You can explore without an account.', 'info')
    return redirect(url_for('dashboard.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    AuthService.logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
