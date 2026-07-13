import pytest
from app import create_app, db
from models.user import User
from models.script import Script


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def auth_client(app, client):
    """Create authenticated test client."""
    with app.app_context():
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        yield client


@pytest.fixture
def sample_script(app, auth_client):
    """Create a sample script for testing."""
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        script = Script(
            title='Test Script',
            content='This is a test script content.',
            user_id=user.id
        )
        script.update_metrics()
        db.session.add(script)
        db.session.commit()
        
        return script
