# Train Station API Service

## Overview

This project implements a comprehensive system for managing trains, journeys, crew, and stations. The API allows travelers to easily book tickets for upcoming train trips. The following sections outline the database structure and provide instructions for setting up and using the service.

## Database Structure

The database consists of the following tables:

![Database Structure](https://media.mate.academy/train_session_diagram_a620513487.png)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/twonumberfortyfives/train-station-api-service.git
   cd train-station-api
   python -m venv venv
   source venv/bin/activate
2. Install requirements:
   ```bash
   pip install -r requirements.txt
3. Set your db settings and project secret key:
   ```bash
   set POSTGRES_HOST = <your db hostname>
   set POSTGRES_NAME = <your db name>
   set POSTGRES_USER = <your db username>
   set POSTGRES_PASSWORD = <your db password>
   set SECRET_KEY = <your secret key>
4. Start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver

## Getting access
- create user via /api/user/register
- get access token via /api/user/token

## Setup with Docker
1. docker-compose build
2. docker-compose up

## Features
- JWT authentication
- Admin panel /admin/
- Documentation is located at api/schema/swagger-ui/ and api/schema/redoc/ (download the schema: api/schema)
- Managing orders and tickets 
- Creating Routes, Journeys, Trains
- Filtering data by names and date
