import os
import sys

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Create Flask application
from app import create_app

application = create_app('production')
