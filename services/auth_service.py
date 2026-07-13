from datetime import datetime
from app import db
from models.user import User
from flask_login import login_user, logout_user


class AuthService:
    
    @staticmethod
    def register_user(email, password, first_name, last_name):
        existing_user = User.query.filter_by(email=email.lower()).first()
        if existing_user:
            return None, "An account with this email already exists."
        
        user = User(
            email=email.lower(),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email.lower()).first()
        if user and user.check_password(password):
            return user, None
        return None, "Invalid email or password."
    
    @staticmethod
    def login_user(user, remember=False):
        login_user(user, remember=remember)
        user.last_login = datetime.utcnow()
        db.session.commit()
    
    @staticmethod
    def logout_user():
        logout_user()
    
    @staticmethod
    def create_guest_user():
        guest = User(
            email=f"guest_{datetime.utcnow().timestamp()}@scriptflow.app",
            password_hash="",
            first_name="Guest",
            last_name="",
            is_guest=True
        )
        db.session.add(guest)
        db.session.commit()
        return guest
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def update_user_theme(user, theme):
        user.theme = theme
        db.session.commit()
        return user
    
    @staticmethod
    def update_user_profile(user, first_name=None, last_name=None):
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        db.session.commit()
        return user
