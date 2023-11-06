from flask import Flask, request, jsonify
from . import app
from models import db

app = Flask(__name__)

# Car CRUD endpoints
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    query = "CREATE (car:Car {id: $id, make: $make, model: $model, year: $year, location: $location, status: 'available'}) RETURN car"
    result = db.query(query, data)
    return jsonify(result[0]['car']), 201

@app.route('/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    query = "MATCH (car:Car {id: $id}) RETURN car"
    result = db.query(query, {'id': car_id})
    return jsonify(result[0]['car']), 200 if result else 404

@app.route('/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    query = "MATCH (car:Car {id: $id}) SET car += $properties RETURN car"
    result = db.query(query, {'id': car_id, 'properties': data})
    return jsonify(result[0]['car']), 200 if result else 404

@app.route('/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    query = "MATCH (car:Car {id: $id}) DETACH DELETE car"
    db.query(query, {'id': car_id})
    return jsonify({"message": "Car deleted"}), 200

# Specific functionality endpoints
@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    query = """
    MATCH (car:Car {id: $car_id, status: 'available'})
    SET car.status = 'booked'
    RETURN car
    """
    result = db.query(query, data)
    return jsonify({"message": "Order placed", "car": result[0]['car']}), 200 if result else 404

@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.get_json()
    query = "MATCH (car:Car {id: $car_id, status: 'booked'}) SET car.status = 'available' RETURN car"
    result = db.query(query, data)
    return jsonify({"message": "Order canceled", "car": result[0]['car']}), 200 if result else 404

@app.route('/rent-car', methods=['POST'])
def rent_car():
    data = request.get_json()
    query = "MATCH (car:Car {id: $car_id, status: 'booked'}) SET car.status = 'rented' RETURN car"
    result = db.query(query, data)
    return jsonify({"message": "Car rented", "car": result[0]['car']}), 200 if result else 404

@app.route('/return-car', methods=['POST'])
def return_car():
    data = request.get_json()
    status = data.get('status', 'available')  # Default to 'available' if not specified
    query = "MATCH (car:Car {id: $car_id, status: 'rented'}) SET car.status = $status RETURN car"
    result = db.query(query, {'car_id': data['car_id'], 'status': status})
    return jsonify({"message": "Car returned", "car": result[0]['car']}), 200 if result else 404

if __name__ == '__main__':
    app.run(debug=True)
