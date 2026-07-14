from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from functools import wraps
from app import db
from models.user import User
from models.script import Script

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def index():
    """Admin dashboard."""
    stats = {
        'total_users': User.query.count(),
        'total_scripts': Script.query.count(),
        'total_words': db.session.query(db.func.sum(Script.word_count)).scalar() or 0,
        'active_users': User.query.filter_by(is_guest=False).count()
    }
    return render_template('admin/index.html', stats=stats)


@admin_bp.route('/users')
@admin_required
def users():
    """View all users."""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user."""
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin.users'))
    
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'error')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/scripts')
@admin_required
def scripts():
    """View all scripts."""
    page = request.args.get('page', 1, type=int)
    per_page = 30
    scripts = Script.query.order_by(Script.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/scripts.html', scripts=scripts)


@admin_bp.route('/database')
@admin_required
def database():
    """Database stats."""
    import os
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'database.db')
    db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    
    stats = {
        'db_size': db_size,
        'db_size_mb': round(db_size / (1024 * 1024), 2),
        'total_users': User.query.count(),
        'total_scripts': Script.query.count(),
        'guest_users': User.query.filter_by(is_guest=True).count()
    }
    return render_template('admin/database.html', stats=stats)
