## Quick start with Docker

1. **Clone the repository:**

    ```bash
    git clone https://github.com/F-redy/homework_for_geekhub.git
    ```
2. **Navigate to the project directory:**

   ```bash
    cd homework_for_geekhub/HT_24/sears-api-tests
    ```

3. **Set up environment variables:**

    - Create a `.env` file in the root directory based on `.env-example`.
    - Fill in the actual values for your local setup in the `.env` file.
   ### `.env-example`

   The `.env-example` file contains examples of the required environment variables:
   
   ```plaintext
    SECRET_KEY=enter_yor_key
    DEBUG=on
    REDIS_URL=redis://redis:6379
   ```

4. **Start the development server:**

    ```bash
    docker-compose up -d --build
    ```
   or
   ```bash
    docker-compose up --build
    ```