import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app using importlib for compatibility
from importlib import import_module

# Import the app module
app_module = import_module('app')

# Get the Flask application
application = app_module.create_app('production')
