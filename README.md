# Fitness Studio Booking API

A simple and robust RESTful API for a fictional fitness studio, built with Python, FastAPI, and SQLAlchemy. This API allows clients to view upcoming classes, book a spot, and check their existing bookings.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0+-green.svg)
![Alembic](https://img.shields.io/badge/Alembic-1.16.0+-orange.svg)
![Pytest](https://img.shields.io/badge/tests-pytest-blueviolet)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
  - [1. Database Migrations](#1-database-migrations)
  - [2. Start the Server](#2-start-the-server)
- [Running Tests](#running-tests)
- [API Endpoints Documentation](#api-endpoints-documentation)
  - [Get All Classes](#1-get-classes)
  - [Book a Class](#2-post-book)
  - [Get Bookings by Email](#3-get-bookings)
- [Key Design Choices](#key-design-choices)

## Features

- **View Classes**: Get a list of all available fitness classes.
- **Book a Spot**: Book a spot in a class for a client.
- **View Bookings**: Retrieve all bookings made by a specific client.
- **Input Validation**: Robust validation for request bodies and parameters using Pydantic.
- **Error Handling**: Clear error messages for edge cases like overbooking or invalid data.
- **Timezone Aware**: Class times are managed correctly using a dedicated timezone utility.
- **Database Migrations**: Uses Alembic to manage database schema changes.
- **Initial Data Loading**: Automatically populates the database with classes from a JSON file on first run.
- **Unit Tests**: Includes a suite of tests written with `pytest`.

## Project Structure

```
.
├── alembic/     # Alembic migration scripts
│ └── versions/
├── app/         # Main application source code
│ ├── crud/      # Database CRUD logic
│ ├── data/      # Static data for initial data loading
│ ├── routers/   # API endpoint definitions
│ ├── tests/     # Unit and integration tests
│ ├── utils/     # Shared helper functions
│ └── init.py
├── .env         # Environment variables
├── .gitignore
├── alembic.ini  # Alembic configuration
├── database.py  # SQLAlchemy engine and session setup
├── initial_data_loading.py  # Script to populate DB with initial data
├── main.py     # FastAPI application entry point
├── models.py   # SQLAlchemy ORM models
├── README.md   # Readme file
├── requirements.txt  # Python dependencies
├── sample.env        # Example environment file
└── schemas.py        # Pydantic data models for validation
```

## Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

- Python 3.9+
- `pip` package manager
- A virtual environment tool like `venv` (recommended)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Abhinav7558/BookingAPI.git
    cd fitness-booking-api
    ```

2.  **Create and activate a virtual environment:**

    - **On macOS/Linux:**
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - **On Windows:**
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **(Optional) Create an environment file** from the sample:
    ```bash
    cp sample.env .env
    ```

## Running the Application

Once the installation is complete, follow these two steps to run the API server.

### 1. Database Migrations

This project uses **Alembic** to manage the SQLite database schema. The first time you run the application, you need to apply the migrations.

Run the following command to create the database (`fitness_studio.db`) and set up the tables:

```bash
alembic upgrade head
```

## 2. Start the Server

Now, start the API server using Uvicorn. The `--reload` flag will automatically restart the server whenever you make changes to the code. Since `main.py` is in the root directory, the command is:

```bash
uvicorn app.main:app --reload
```

On the initial startup, the server will automatically populate the database with fitness classes from `app/data/classes.json`.

The API will now be running and accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000)

You can access the interactive API documentation (powered by Swagger UI) at:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 3. Running Tests

This project uses `pytest` for unit testing. To run the full test suite, execute the following command in your terminal:

```bash
pytest
```

The tests will run against a separate, in-memory SQLite database to avoid interfering with your development data.

---

## 4. API Endpoints Documentation

### 1. `GET /classes`

Returns a list of all upcoming fitness classes.

- **URL**: `/classes`
- **Method**: `GET`
- **Query Parameters**:
  - `tz` (optional): A valid timezone string (e.g., `America/New_York`, `Europe/London`) to display class times in that timezone. Defaults to UTC.

#### **Success Response (200 OK):**

```json
[
  {
    "id": 1,
    "name": "Yoga",
    "instructor": "Yoga Instructor 1",
    "scheduled_at": "2025-07-01T04:30:00",
    "total_slots": 5,
    "available_slots": 5
  }
]
```

---

### 2. `POST /bookings`

Books a spot in a specific class for a client.

- **URL**: `/bookings`
- **Method**: `POST`
- **Request Body**:

```json
{
  "class_id": 1,
  "client_name": "user",
  "client_email": "user@example.com"
}
```

#### **Success Response (201 Created):**

```json
{
  "class_id": 1,
  "client_name": "user",
  "client_email": "user@example.com",
  "id": 1,
  "booking_time": "2025-06-10T16:06:56",
  "scheduled_at": "2025-07-01T00:30:00",
  "status": "confirmed"
}
```

#### **Error Responses:**

- `404`: Class not found
- `409`: Class full
- `422`: Invalid input

---

### 3. `GET /bookings`

Returns all bookings made by a specific client, identified by their email address.

- **URL**: `/bookings`
- **Method**: `GET`
- **Query Parameters**:
  - `client_email` (required): The email address of the client.
    `time_zone` (optional): Timezone to show the results.

#### **Example Request:**

```
GET /bookings/?client_email=user@example.com
```

#### **Success Response (200 OK):**

```json
[
  {
    "class_id": 1,
    "client_name": "user",
    "client_email": "user@example.com",
    "id": 1,
    "booking_time": "2025-06-10T21:36:56",
    "scheduled_at": "2025-07-01T06:00:00",
    "status": "confirmed",
    "class_name": "Yoga",
    "instructor": "Yoga Instructor 1"
  }
]
```

---

## Key Design Choices

- **Framework**:  
  FastAPI was chosen for its high performance, automatic interactive documentation, and excellent data validation with Pydantic.

- **Database**:  
  SQLite is used for simplicity, with SQLAlchemy as the ORM.

- **Modularity**:  
  The application is organized with a clear separation of concerns:

  - The `app/` directory contains:
    - Business logic (`crud`)
    - API routes (`routers`)
    - Utilities (`utils`)
  - Core files like `main.py`, `database.py`, `models.py`, and `schemas.py` are at the project root for clear entry points and definitions.

- **Data Seeding**:  
  A script (`initial_data_loading.py`) loads class data from a clean `classes.json` file on startup, making it easy to manage and reset test data.

- **Timezone Management**:  
  All datetimes are handled in a timezone-aware manner, with a dedicated utility module ensuring consistency. Classes are assumed to be created in IST and stored as UTC.
