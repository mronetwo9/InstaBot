import os
import sys

import django
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'config.env')
load_dotenv(env_path)


TOKEN = os.getenv('TOKEN')

PARENT_PACKAGE = '..'
APP_PACKAGE = 'server'
PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
APP_DIR = os.path.join(PARENT_DIR, APP_PACKAGE)

sys.path.append(APP_DIR)
sys.path.append(PARENT_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
