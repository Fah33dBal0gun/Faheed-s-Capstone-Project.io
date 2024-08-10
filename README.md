# Movie Listing API

This is a FastAPI-based project for a movie listing API. The API allows users to list movies, view listed movies, rate them, and add comments. The application is secured using JWT (JSON Web Tokens), ensuring that only the user who listed a movie can edit or delete it.

## Features

- *User Authentication:*
  - User registration
  - User login
  - JWT token generation for secured endpoints

- *Movie Listing:*
  - List a movie (authenticated users only)
  - View all movies (public access)
  - Edit a movie (only by the user who listed it)
  - Delete a movie (only by the user who listed it)

- *Movie Rating:*
  - Rate a movie (public access)
  - Get ratings for a movie

- *Comments:*
  - Add a comment to a movie (public access)
  - View comments for a movie (public access)

## Project Structure

```plaintext
movie_listing_api/
├── alembic/              # Alembic migration files
├── app/                  # Application files
│   ├── _init_.py
│   ├── main.py           # Main application entry point
│   ├── routers.py        # API route definitions
│   ├── schemas.py        # Pydantic schemas for data validation
│   ├── models.py         # SQLAlchemy models representing the database
│   ├── database.py       # Database connection and session management
│   ├── .env              # Environment variables (if any)
├── README.md             # This README file
├── requirements.txt      # Project dependencies
└── alembic.ini           # Alembic configuration file
