"""
Utility functions for FastAPI application
"""

import os
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()


def get_file_url(file_path):
    """Convert file path to URL"""
    if file_path:
        return f"/media/{file_path}"
    return None
