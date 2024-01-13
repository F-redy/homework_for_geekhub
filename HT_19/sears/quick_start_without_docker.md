## Quick start without Docker

1. **Clone the repository:**

    ```bash
    git clone https://github.com/F-redy/homework_for_geekhub.git
    ```
2. **Navigate to the project directory:**

   ```bash
    cd homework_for_geekhub/HT_19/sears
    ```
3. **Create a virtual environment:**
   For Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

   For Unix or macOS:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. **Install the required packages:**

    ```bash
    pip install -r requirements/development.txt
    ```

5. **Set up environment variables:**

    - Create a `.env` file in the root directory based on `.env-example`.
    - Fill in the actual values for your local setup in the `.env` file.
   ### `.env-example`

   The `.env-example` file contains examples of the required environment variables:
   
   ```plaintext
    SECRET_KEY=enter_yor_key
    DEBUG=on
    DATABASE_URL=postgres://db_user:db_password@db/db_name
   ```
   **Note:**
   
    Ensure you configure the database properly by updating `DATABASE_URL` with your PostgreSQL credentials.

   ### Setting Postgres:

   [Django Docs](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DATABASES)   

   ### Alternatively
 
    You can switch to `SQLite` in the [settings](./settings/base.py) file:

   **paste:**

    ```plaintext
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
   ```

   **delete:**

    ```plaintext
    DATABASES = {
        "default": env.db('DATABASE_URL')
    }
   ```

6. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

7. **Create superuser:**

   ```bash
    python manage.py createsuperuser
    ```
   Follow the prompts to enter a username, email (optional), and password for the superuser.

8. **Start the development server:**

    ```bash
    python manage.py runserver
    ```