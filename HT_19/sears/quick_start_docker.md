## Quick start with Doker

1. **Clone the repository:**

    ```bash
    git clone https://github.com/F-redy/homework_for_geekhub.git
    ```
2. **Navigate to the project directory:**

   ```bash
    cd homework_for_geekhub/HT_19/sears
    ```

3.  **Set up environment variables:**

    - Create a `.env` file in the root directory based on `.env-example`.
    - Fill in the actual values for your local setup in the `.env` file.
    ### `.env-example`

   The `.env-example` file contains examples of the required environment variables:
   
   ```plaintext
    SECRET_KEY=enter_yor_key
    DEBUG=on
    DATABASE_URL=postgres://db_user:db_password@db/db_name
   ```
   
4. **Start project:**

   ### Prerequisites

   Make sure you have Docker and Docker Compose installed on your machine.

   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

   ```bash
    bin/setup
   ```
