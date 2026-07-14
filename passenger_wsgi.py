import os
import sys

# Ensure instance directory exists
instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Create Flask application
from app import create_app

application = create_app('production')
