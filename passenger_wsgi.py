import sys
import os

INTERP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

application = create_app()
