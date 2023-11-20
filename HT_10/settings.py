import os

ROOT_DIR = os.path.dirname(__file__)

DB_PATH = DATA_USERS = os.path.join(ROOT_DIR, 'atm_management.db')
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR, 'db_scripts.sql')

ALLOWED_CURRENCY = (10, 20, 50, 100, 200, 500, 1000)
