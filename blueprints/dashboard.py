from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from services.script_service import ScriptService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    scripts = ScriptService.get_user_scripts(current_user.id)[:6]
    favorites = ScriptService.get_favorite_scripts(current_user.id)[:4]
    stats = ScriptService.get_statistics(current_user.id)
    
    return render_template('dashboard/index.html', 
                         scripts=scripts,
                         favorites=favorites,
                         stats=stats)


@dashboard_bp.route('/scripts')
@login_required
def scripts():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    sort_by = request.args.get('sort', 'updated_at')
    filter_type = request.args.get('filter', 'all')
    search_query = request.args.get('q', '')
    
    scripts = ScriptService.get_user_scripts(current_user.id)
    
    if search_query:
        scripts = ScriptService.search_scripts(current_user.id, search_query)
    elif filter_type == 'favorites':
        scripts = ScriptService.get_favorite_scripts(current_user.id)
    
    if sort_by == 'title':
        scripts = sorted(scripts, key=lambda s: s.title.lower())
    elif sort_by == 'word_count':
        scripts = sorted(scripts, key=lambda s: s.word_count)
    elif sort_by == 'created_at':
        scripts = sorted(scripts, key=lambda s: s.created_at, reverse=True)
    
    return render_template('dashboard/scripts.html',
                         scripts=scripts,
                         sort_by=sort_by,
                         filter_type=filter_type,
                         search_query=search_query)


@dashboard_bp.route('/script/<int:script_id>')
@login_required
def view_script(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        flash('Script not found.', 'error')
        return redirect(url_for('dashboard.scripts'))
    
    ScriptService.mark_as_opened(script)
    return render_template('dashboard/script-view.html', script=script)


@dashboard_bp.route('/script/<int:script_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_script(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        flash('Script not found.', 'error')
        return redirect(url_for('dashboard.scripts'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            ScriptService.update_script(script, title, content)
            flash('Script saved successfully.', 'success')
            return redirect(url_for('dashboard.view_script', script_id=script.id))
    
    return render_template('dashboard/script-edit.html', script=script)


@dashboard_bp.route('/script/<int:script_id>/editor')
@login_required
def script_editor(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        flash('Script not found.', 'error')
        return redirect(url_for('dashboard.scripts'))
    
    return render_template('dashboard/script-editor.html', script=script)


@dashboard_bp.route('/script/create', methods=['GET', 'POST'])
@login_required
def create_script():
    if request.method == 'POST':
        title = request.form.get('title', 'Untitled Script')
        content = request.form.get('content', '')
        script = ScriptService.create_script(current_user.id, title, content)
        flash('Script created successfully.', 'success')
        return redirect(url_for('dashboard.edit_script', script_id=script.id))
    
    return render_template('dashboard/script-create.html')


@dashboard_bp.route('/profile')
@login_required
def profile():
    stats = ScriptService.get_statistics(current_user.id)
    return render_template('dashboard/profile.html', stats=stats)


@dashboard_bp.route('/settings')
@login_required
def settings():
    return render_template('dashboard/settings.html')
