
from flask import Flask, request, jsonify
from .import app
from .models import db

# Car CRUD Endpoints
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.get_json()
    result = db.query("CREATE (car:Car $props) RETURN car", {'props': data})
    # Convert the Neo4j Node to a dictionary
    serialized_result = [{key: value for key, value in record['car'].items()} for record in result]
    return jsonify(serialized_result), 201


@app.route('/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    result = db.query("MATCH (car:Car) WHERE id(car) = $id RETURN car", {'id': int(car_id)})
    return jsonify(result), 200 if result else 404

@app.route('/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    result = db.query("MATCH (car:Car) WHERE id(car) = $id SET car += $props RETURN car", {'id': int(car_id), 'props': data})
    return jsonify(result), 200 if result else 404

@app.route('/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    result = db.query("MATCH (car:Car) WHERE id(car) = $id DETACH DELETE car", {'id': int(car_id)})
    return jsonify({'message': 'Car deleted'}), 200 if result else 404

# Customer CRUD Endpoints
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    result = db.query("CREATE (customer:Customer $props) RETURN customer", {'props': data})
    return jsonify(result), 201

@app.route('/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    result = db.query("MATCH (customer:Customer {id: $id}) RETURN customer", {'id': customer_id})
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404

@app.route('/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    result = db.query(
        "MATCH (customer:Customer {id: $id}) "
        "SET customer += $props "
        "RETURN customer",
        {'id': customer_id, 'props': data}
    )
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404

@app.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    result = db.query("MATCH (customer:Customer {id: $id}) DETACH DELETE customer", {'id': customer_id})
    if result:
        return jsonify({'message': 'Customer deleted'}), 200
    else:
        return jsonify({'message': 'Customer not found'}), 404

# Order Car Endpoint
@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.get_json()
    customer_id = data.get('customer_id')
    car_id = data.get('car_id')
    if not customer_id or not car_id:
        return jsonify({'message': 'Missing customer_id or car_id'}), 400
    result = db.query(
        "MATCH (customer:Customer {id: $customer_id}), (car:Car {id: $car_id}) "
        "WHERE NOT (customer)-[:BOOKED]->(:Car) AND car.status = 'available' "
        "CREATE (customer)-[:BOOKED]->(car) "
        "SET car.status = 'booked' "
        "RETURN car",
        {'customer_id': customer_id, 'car_id': car_id}
    )
    if result:
        return jsonify({'message': 'Car booked successfully', 'car': result}), 200
    else:
        return jsonify({'message': 'Booking failed'}), 400


@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    result = db.query("CREATE (employee:Employee $props) RETURN employee", {'props': data})
    return jsonify(result), 201

@app.route('/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    result = db.query("MATCH (employee:Employee {id: $id}) RETURN employee", {'id': employee_id})
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    result = db.query(
        "MATCH (employee:Employee {id: $id}) "
        "SET employee += $props "
        "RETURN employee",
        {'id': employee_id, 'props': data}
    )
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    result = db.query("MATCH (employee:Employee {id: $id}) DETACH DELETE employee", {'id': employee_id})
    if result:
        return jsonify({'message': 'Employee deleted'}), 200
    else:
        # If nothing was deleted, assume the employee was not found
        return jsonify({'message': 'Employee not found'}), 404.


if __name__ == '__main__':
    app.run(debug=True)

