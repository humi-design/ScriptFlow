from datetime import datetime
from app import db


class Script(db.Model):
    __tablename__ = 'scripts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    is_favorite = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    word_count = db.Column(db.Integer, default=0)
    estimated_read_time = db.Column(db.Integer, default=0)
    scroll_speed = db.Column(db.Float, default=50)
    font_size = db.Column(db.Integer, default=32)
    line_height = db.Column(db.Float, default=1.8)
    theme = db.Column(db.String(32), default='dark')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_opened_at = db.Column(db.DateTime)
    
    @staticmethod
    def calculate_read_time(word_count, words_per_minute=150):
        return max(1, round(word_count / words_per_minute))
    
    @staticmethod
    def count_words(text):
        if not text:
            return 0
        return len(text.split())
    
    def update_metrics(self):
        self.word_count = self.count_words(self.content)
        self.estimated_read_time = self.calculate_read_time(self.word_count)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'word_count': self.word_count,
            'estimated_read_time': self.estimated_read_time,
            'is_favorite': self.is_favorite,
            'scroll_speed': self.scroll_speed,
            'font_size': self.font_size,
            'line_height': self.line_height,
            'theme': self.theme,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_opened_at': self.last_opened_at.isoformat() if self.last_opened_at else None
        }
    
    def __repr__(self):
        return f'<Script {self.id}: {self.title}>'
