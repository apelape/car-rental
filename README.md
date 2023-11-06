
```markdown
# Car Rental Web-API

This project is a Flask web-API for a car rental service, interfacing with a Neo4j graph database. The API allows managing a fleet of cars, customers, and employees, as well as processing car rentals.

## Prerequisites

- Python 3
- Flask
- Neo4j Database

Ensure Neo4j is running and accessible at the URI provided in your `models.py`.

## Setup

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/apelape/car-rental.git
cd car-rental
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application with:

```bash
python run.py
```

The API will be available at `http://localhost:5001`.

## API Endpoints

The following endpoints are available:

- `POST /cars` - Create a new car record.
- `GET /cars/<car_id>` - Retrieve a car's details.
- `PUT /cars/<car_id>` - Update a car's details.
- `DELETE /cars/<car_id>` - Delete a car record.
- Similar endpoints exist for `customers` and `employees`.
- `POST /order-car` - Process a car booking.

## Testing

Test the API endpoints using a tool like Postman or curl.

