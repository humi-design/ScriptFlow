#!/usr/bin/env python3
"""ScriptFlow Database Initialization Script"""
import os
import sys

instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

sys.path.insert(0, os.path.dirname(__file__))
from app import create_app, db

def init_database():
    app = create_app('production')
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        print("\nScriptFlow is ready!")

if __name__ == '__main__':
    init_database()
