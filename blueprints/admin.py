from flask import Blueprint, render_template, request, redirect, url_for, flash
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
        # For now, allow any authenticated user
        # In production, check for admin role
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
    
    users = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user and their scripts."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'error')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {user.email} has been deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/scripts')
@admin_required
def scripts():
    """View all scripts."""
    page = request.args.get('page', 1, type=int)
    per_page = 30
    
    scripts = Script.query.order_by(Script.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/scripts.html', scripts=scripts)


@admin_bp.route('/scripts/<int:script_id>/delete', methods=['POST'])
@admin_required
def delete_script(script_id):
    """Delete a script."""
    script = Script.query.get_or_404(script_id)
    
    db.session.delete(script)
    db.session.commit()
    
    flash('Script has been deleted.', 'success')
    return redirect(url_for('admin.scripts'))


@admin_bp.route('/database')
@admin_required
def database():
    """Database health and stats."""
    # Get database file size
    import os
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database.db')
    db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
    
    stats = {
        'db_size': db_size,
        'db_size_mb': round(db_size / (1024 * 1024), 2),
        'total_users': User.query.count(),
        'total_scripts': Script.query.count(),
        'guest_users': User.query.filter_by(is_guest=True).count(),
        'favorite_scripts': Script.query.filter_by(is_favorite=True).count()
    }
    
    return render_template('admin/database.html', stats=stats)


@admin_bp.route('/export')
@admin_required
def export_database():
    """Export database as JSON for backup."""
    import json
    from flask import Response
    
    users_data = [{
        'id': u.id,
        'email': u.email,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'is_guest': u.is_guest,
        'created_at': u.created_at.isoformat() if u.created_at else None
    } for u in User.query.all()]
    
    scripts_data = [{
        'id': s.id,
        'title': s.title,
        'content': s.content,
        'user_id': s.user_id,
        'word_count': s.word_count,
        'is_favorite': s.is_favorite,
        'created_at': s.created_at.isoformat() if s.created_at else None,
        'updated_at': s.updated_at.isoformat() if s.updated_at else None
    } for s in Script.query.all()]
    
    export_data = {
        'version': '1.0.0',
        'exported_at': datetime.utcnow().isoformat(),
        'users': users_data,
        'scripts': scripts_data
    }
    
    response = Response(
        json.dumps(export_data, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=scriptflow_backup.json'}
    )
    
    return response


from datetime import datetime
