
# Notes Application Backend
A robust backend service built with FastAPI, designed to manage user authentication and personal notes.

## Features
- **User Authentication**: Secure registration and login using JWT (JSON Web Tokens).
- **Note Management**: CRUD operations for personal notes (Create, Read, Update, Delete).
- **Database**: Managed via SQLite using SQLModel for object-relational mapping and Alembic for database migrations.

## Installation

1. **Clone the repository** and navigate to the project folder:
   ```bash
   cd notes

```

2. **Create and activate your virtual environment**:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate

```


3. **Install dependencies**:
```bash
pip install fastapi uvicorn sqlmodel alembic bcrypt python-jose[cryptography] python-multipart

```

## Database Setup & Migrations
We use **Alembic** to manage database schema changes.

1. **Initialize the Database**:
Apply existing migrations to create your tables:
```bash
alembic upgrade head

```

2. **Applying Schema Changes**:
Whenever you modify your models in `app/models.py`, update the database with these steps:
```bash
# Generate a new migration script
alembic revision --autogenerate -m "Description of changes"

# Apply the changes to the database
alembic upgrade head

```

## Running the Application
Start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload

```
Access the interactive API documentation (Swagger UI) at: `http://127.0.0.1:8000/docs`
## API Usage Quick Reference

* **Register**: `POST /register`
* Send: `{"username": "your_username", "password": "your_password"}`


* **Login**: `POST /token`
* Send (as `x-www-form-urlencoded`): `username`, `password`, `grant_type`


* **Create Note**: `POST /notes`
* Requires Bearer Token authorization.
* Send: `{"title": "Note Title", "content": "Note Content"}`

## Docker Setup & Installation

To run this application using Docker, ensure you have Docker installed on your system[cite: 1].

### 1. Configure Environment Variables
Create a `.env` file in the root directory and add your required configuration variables (such as database URLs and secret keys):
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=your_database_url_here

docker build -t notes-app .
[cite: 1]

### 3. Run the Container
Start the container and map port 8000 using your `.env` file:
```bash
docker run -d --name notes-container --env-file .env -p 8000:8000 notes-app
[cite: 1]

### 4. Access the API
Once the container is running, open your browser and navigate to:
* **Swagger UI Documentation:** `http://localhost:8000/docs`