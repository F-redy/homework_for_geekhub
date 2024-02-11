## Quick start without Docker

1. **Clone the repository:**

    ```bash
    git clone https://github.com/F-redy/homework_for_geekhub.git
    ```
2. **Navigate to the project directory:**

   ```bash
    cd homework_for_geekhub/HT_22/sears-js
    ```
3. **Create a virtual environment:**
   For Windows:

    ```bash
    python -m venv venv
    venv/Scripts/activate
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
   ```

6. **Start the development server:**

    ```bash
    python manage.py runserver
    ```