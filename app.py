import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name='production'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'production' or config_name is None:
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'development':
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    else:
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import models
    from models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        # Ensure instance directory exists
        instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)
        
        db.create_all()
    
    # Register blueprints
    from blueprints.auth import auth_bp
    from blueprints.dashboard import dashboard_bp
    from blueprints.api import api_bp
    from blueprints.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Routes
    @app.route('/')
    def index():
        return render_template('landing.html')
    
    return app


# For running directly with `python app.py`
if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)
