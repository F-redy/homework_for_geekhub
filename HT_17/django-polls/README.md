# Tutorial-project with Django

This is a tutorial project created with Django.

## Documentation

The official Django documentation for version 5.0 can be found [here](https://docs.djangoproject.com/en/5.0/).

## Quick start

1. **Clone the repository:**

    ```bash
    git clone https://github.com/F-redy/homework_for_geekhub.git
    ```
2. **Navigate to the project directory:**

   ```bash
    cd HT_17
    ```
3. **Create a virtual environment:**
   For Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    For Unix or MacOS:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```
5. **Navigate to the project directory:**
   ```bash
    cd django-polls
    ```
   
6. **Set up environment variables:**

    - Create a `.env` file in the root directory based on `.env-example`.
    - Fill in the actual values for your local setup in the `.env` file.
   ### `.env-example`

   The `.env-example` file contains examples of the required environment variables:
   
   ```plaintext
   # Database configuration
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_PORT=your_db_port
   
   # Other settings
   SECRET_KEY=your_secret_key
   ```
   
7. **Run migrations:**

    ```bash
    python manage.py migrate
    ```
8. **Create superuser:**
   ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to enter a username, email (optional), and password for the superuser.

9. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

10. **Access the development server:**

    - Open a web browser and go to http://127.0.0.1:8000/admin/ to create a poll.
    - Visit http://127.0.0.1:8000/polls/ to participate in the poll.