from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from services.script_service import ScriptService
from services.auth_service import AuthService
from app import db

api_bp = Blueprint('api', __name__)


@api_bp.route('/scripts', methods=['GET'])
@login_required
def get_scripts():
    scripts = ScriptService.get_user_scripts(current_user.id)
    return jsonify({
        'success': True,
        'scripts': [s.to_dict() for s in scripts]
    })


@api_bp.route('/scripts', methods=['POST'])
@login_required
def create_script():
    data = request.get_json()
    title = data.get('title', 'Untitled Script')
    content = data.get('content', '')
    
    script = ScriptService.create_script(current_user.id, title, content)
    
    return jsonify({
        'success': True,
        'script': script.to_dict()
    })


@api_bp.route('/scripts/<int:script_id>', methods=['GET'])
@login_required
def get_script(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        return jsonify({'success': False, 'error': 'Script not found'}), 404
    
    return jsonify({
        'success': True,
        'script': script.to_dict()
    })


@api_bp.route('/scripts/<int:script_id>', methods=['PUT'])
@login_required
def update_script(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        return jsonify({'success': False, 'error': 'Script not found'}), 404
    
    data = request.get_json()
    
    title = data.get('title')
    content = data.get('content')
    
    if title is not None:
        script.title = title
    if content is not None:
        script.content = content
    
    script.update_metrics()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'script': script.to_dict()
    })


@api_bp.route('/scripts/<int:script_id>', methods=['DELETE'])
@login_required
def delete_script(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        return jsonify({'success': False, 'error': 'Script not found'}), 404
    
    ScriptService.soft_delete_script(script)
    
    return jsonify({'success': True})


@api_bp.route('/scripts/<int:script_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        return jsonify({'success': False, 'error': 'Script not found'}), 404
    
    script = ScriptService.toggle_favorite(script)
    
    return jsonify({
        'success': True,
        'is_favorite': script.is_favorite
    })


@api_bp.route('/scripts/<int:script_id>/duplicate', methods=['POST'])
@login_required
def duplicate_script(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        return jsonify({'success': False, 'error': 'Script not found'}), 404
    
    new_script = ScriptService.duplicate_script(script, current_user.id)
    
    return jsonify({
        'success': True,
        'script': new_script.to_dict()
    })


@api_bp.route('/scripts/<int:script_id>/settings', methods=['PUT'])
@login_required
def update_settings(script_id):
    script = ScriptService.get_script(script_id, current_user.id)
    if not script:
        return jsonify({'success': False, 'error': 'Script not found'}), 404
    
    data = request.get_json()
    script = ScriptService.update_script_settings(script, **data)
    
    return jsonify({
        'success': True,
        'script': script.to_dict()
    })


@api_bp.route('/user/theme', methods=['PUT'])
@login_required
def update_theme():
    data = request.get_json()
    theme = data.get('theme', 'dark')
    
    user = AuthService.update_user_theme(current_user, theme)
    
    return jsonify({
        'success': True,
        'theme': user.theme
    })


@api_bp.route('/user/stats', methods=['GET'])
@login_required
def get_stats():
    stats = ScriptService.get_statistics(current_user.id)
    return jsonify({
        'success': True,
        'stats': stats
    })


@api_bp.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '')
    scripts = ScriptService.search_scripts(current_user.id, query)
    
    return jsonify({
        'success': True,
        'scripts': [s.to_dict() for s in scripts]
    })
