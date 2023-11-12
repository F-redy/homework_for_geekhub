import os

ROOT_DIR = os.path.dirname(__file__)
DATA_USERS = os.path.join(ROOT_DIR, 'data_users')

for name_dir in [DATA_USERS,
                 os.path.join(ROOT_DIR, DATA_USERS, 'balance'),
                 os.path.join(ROOT_DIR, DATA_USERS, 'transactions'),
                 ]:
    if not os.path.exists(name_dir):
        os.makedirs(name_dir)

# database
# users
DATABASE_USERS = os.path.join(ROOT_DIR, DATA_USERS, 'users.csv')
if not os.path.exists(DATABASE_USERS):
    with open(DATABASE_USERS, 'w', newline='') as f:
        pass
# error
DATABASE_ERROR = os.path.join(ROOT_DIR, DATA_USERS, 'error_log.json')

# balance
DATABASE_BALANCE = os.path.join(ROOT_DIR, DATA_USERS, 'balance')

# transactions
DATABASE_TRANSACTIONS = os.path.join(ROOT_DIR, DATA_USERS, 'transactions')

# users
ATTEMPTS = 3

MIN_LENGTH_USERNAME = 3
MAX_LENGTH_USERNAME = 20

MIN_LETTERS_PASSWORD = 1
MIN_LENGTH_PASSWORD = 8

# system messages
CONTACT_SUPPORT = 'Зверніться до служби підтримки.\ntelegram: @F_redy\nphone:+380 99 169 79 86'
