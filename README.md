# Backend_FASTApi

# Installing Steps
1. Clone the repository

```bash
git clone https://github.com/knocBack/Backend_FASTApi.git
cd Backend_FASTApi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Running the FastAPI Application:

Run Development Server:
```bash
uvicorn app.main:app --reload
```

Run Production Server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

# Installing PostgreSQL on Windows:
### Download and Install PostgreSQL:
- Visit the official [PostgreSQL download page]<https://www.postgresql.org/download/> and download the installer for Windows.
- Run the installer and follow the installation instructions.
- During the installation, you will be prompted to set a password for the postgres superuser. Choose a strong password and remember it for later use.
### Set Environment Variables:
- Open .env file in the project dir and update the corresponding values
    - DATABASE_HOSTNAME: Set to "localhost".
    - DATABASE_PORT: Set to "5432" (the default PostgreSQL port).
    - DATABASE_PASSWORD: Set to your PostgreSQL password.
    - DATABASE_NAME: Set to "backend_assignment" (your desired database name).
    - DATABASE_USERNAME: Set to "username" (your PostgreSQL username).
    - SECRET_KEY: Set to your desired secret key for the application.
    - ALGORITHM: Set to "HS256" (the JWT algorithm).
    - ACCESS_TOKEN_EXPIRE_MINUTES: Set to 30 (or your desired token expiration time).

# Installing PostgreSQL on macOS:
### Install PostgreSQL using Homebrew:
- Open Terminal (you can find it in Applications > Utilities).
- Install Homebrew if you haven't already by running:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
- Install PostgreSQL using Homebrew:
```bash
brew install postgresql
```

# Initialize and Start PostgreSQL:
- Start the PostgreSQL server using Homebrew services:
```bash
brew services start postgresql
```
- PostgreSQL will be automatically started and set to launch at login.

### Set Environment Variables:
- Open .env file in the project dir and update the corresponding values
    - DATABASE_HOSTNAME: Set to "localhost".
    - DATABASE_PORT: Set to "5432" (the default PostgreSQL port).
    - DATABASE_PASSWORD: Set to your PostgreSQL password.
    - DATABASE_NAME: Set to "backend_assignment" (your desired database name).
    - DATABASE_USERNAME: Set to "username" (your PostgreSQL username).
    - SECRET_KEY: Set to your desired secret key for the application.
    - ALGORITHM: Set to "HS256" (the JWT algorithm).
    - ACCESS_TOKEN_EXPIRE_MINUTES: Set to 30 (or your desired token expiration time).


# Api Documentation

For api documenatation goto: http://127.0.0.1:8000/docs

# External Libraries Used
1. FastAPI (0.111.0):
    FastAPI is the main framework used for building the API endpoints. It provides a fast, asynchronous web framework for building modern APIs in Python.
2. SQLAlchemy (2.0.29):
    SQLAlchemy is a powerful ORM (Object-Relational Mapping) library used for interacting with databases in Python. It simplifies database operations by providing an abstraction layer over SQL databases.
3. uvicorn (0.29.0):
    uvicorn is an ASGI server implementation that runs FastAPI applications. It provides high-performance asynchronous request handling.
4. pydantic (2.7.1):
    pydantic is used for data validation and parsing in FastAPI. It allows you to define data models with type annotations and performs runtime validation of request data.
5. psycopg2 (2.9.9):
    psycopg2 is a PostgreSQL adapter for Python. It enables Python applications to communicate with PostgreSQL databases and execute SQL queries.
6. passlib (1.7.4):
    passlib is a library used for password hashing and validation. It provides utilities for securely hashing passwords and verifying password hashes.
7. bcrypt (4.1.3):
    bcrypt is another library used for password hashing. It's commonly used for securing user passwords by generating and verifying password hashes.
8. python-jose (3.3.0):
    python-jose is a library used for JSON Web Token (JWT) encoding and decoding. It's commonly used in web applications for authentication and authorization.

# Assumptions
- Any user can either be 'customer' or 'admin'
- Admin has authority to update, delete, patch, any details exclusively products and info
- 