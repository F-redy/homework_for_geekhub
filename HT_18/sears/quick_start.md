## Quick start

1. **Clone the repository:**

    ```bash
    git clone https://github.com/F-redy/homework_for_geekhub.git
    ```
2. **Navigate to the project directory:**

   ```bash
    cd HT_18\sears
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
    pip install -r requirements/production.txt
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

9. **Access the development server:**

    - Visit [add-products](http://127.0.0.1:8000/products/add-products/). And add product IDs for scraping
      from [site](https://www.sears.com/).
        - example ID:
            - `p-A093086676`
            - `p-SPM6458104507`
            - `p-SPM9463331817`
    - On the page [products](http://127.0.0.1:8000/products/). You can see the products after scraping.
    - On the page http://127.0.0.1:8000/products/detail-product/ `id-product`. You can see detailed information about
      the product.
    - On the page [task](http://127.0.0.1:8000/task/). You can read about the project task.
    - On the page [admin-site](http://127.0.0.1:8000/admin/products/product/). You can select any product and change it.