# FastAPI Project

A simple web application built with **FastAPI**, designed for scalable and fast API development.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [License](#license)

---

## Features

- Lightweight and fast framework
- Built-in data validation with Pydantic
- Integrated Swagger and ReDoc API documentation
- Async capabilities for improved performance

---

## Requirements

- Python 3.8+
- `pip` package manager

Install the dependencies listed in the `requirements.txt` file.

---

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt

4. Configure environment variables in the .env file.
    ```.env
    DB_HOST=localhost
    DB_POST=3363
    DB_USERNAME=root
    DB_PASSWORD=password
    DB_NAME=store_house

---

## Running the Application

1. Run the development server:
    ```bash
    uvicorn app.main:app --reload

2. Access the application at:
    - Swagger Docs: http://127.0.0.1:8000/docs
    - ReDoc Docs: http://127.0.0.1:8000/redoc

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Root endpoint |
| POST | /items/ | Create a new item |
| GET | /items/{id} | Retrieve an item by |


## Error

#### error venv\Scripts\activate
    ```bash
    Set-ExecutionPolicy Unrestricted -Scope Process