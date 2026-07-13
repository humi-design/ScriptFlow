from datetime import datetime
from app import db
from models.script import Script


class ScriptService:
    
    @staticmethod
    def create_script(user_id, title, content=""):
        script = Script(
            title=title,
            content=content,
            user_id=user_id
        )
        script.update_metrics()
        db.session.add(script)
        db.session.commit()
        return script
    
    @staticmethod
    def get_script(script_id, user_id):
        return Script.query.filter_by(id=script_id, user_id=user_id, is_deleted=False).first()
    
    @staticmethod
    def get_user_scripts(user_id, include_deleted=False):
        query = Script.query.filter_by(user_id=user_id)
        if not include_deleted:
            query = query.filter_by(is_deleted=False)
        return query.order_by(Script.updated_at.desc()).all()
    
    @staticmethod
    def get_favorite_scripts(user_id):
        return Script.query.filter_by(user_id=user_id, is_favorite=True, is_deleted=False)\
            .order_by(Script.updated_at.desc()).all()
    
    @staticmethod
    def search_scripts(user_id, query):
        return Script.query.filter(
            Script.user_id == user_id,
            Script.is_deleted == False,
            Script.title.ilike(f"%{query}%") | Script.content.ilike(f"%{query}%")
        ).order_by(Script.updated_at.desc()).all()
    
    @staticmethod
    def update_script(script, title=None, content=None):
        if title is not None:
            script.title = title
        if content is not None:
            script.content = content
        script.update_metrics()
        script.updated_at = datetime.utcnow()
        db.session.commit()
        return script
    
    @staticmethod
    def update_script_settings(script, **kwargs):
        allowed_fields = ['scroll_speed', 'font_size', 'line_height', 'theme']
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(script, key, value)
        db.session.commit()
        return script
    
    @staticmethod
    def toggle_favorite(script):
        script.is_favorite = not script.is_favorite
        db.session.commit()
        return script
    
    @staticmethod
    def soft_delete_script(script):
        script.is_deleted = True
        script.deleted_at = datetime.utcnow()
        db.session.commit()
        return script
    
    @staticmethod
    def restore_script(script_id, user_id):
        script = Script.query.filter_by(id=script_id, user_id=user_id, is_deleted=True).first()
        if script:
            script.is_deleted = False
            db.session.commit()
        return script
    
    @staticmethod
    def duplicate_script(script, user_id):
        new_script = Script(
            title=f"{script.title} (Copy)",
            content=script.content,
            user_id=user_id,
            scroll_speed=script.scroll_speed,
            font_size=script.font_size,
            line_height=script.line_height,
            theme=script.theme
        )
        new_script.update_metrics()
        db.session.add(new_script)
        db.session.commit()
        return new_script
    
    @staticmethod
    def mark_as_opened(script):
        script.last_opened_at = datetime.utcnow()
        db.session.commit()
        return script
    
    @staticmethod
    def get_statistics(user_id):
        scripts = Script.query.filter_by(user_id=user_id, is_deleted=False).all()
        total_words = sum(s.word_count for s in scripts)
        total_read_time = sum(s.estimated_read_time for s in scripts)
        favorite_count = sum(1 for s in scripts if s.is_favorite)
        
        return {
            'total_scripts': len(scripts),
            'total_words': total_words,
            'total_read_time': total_read_time,
            'favorite_count': favorite_count,
            'average_words_per_script': total_words // len(scripts) if scripts else 0
        }
