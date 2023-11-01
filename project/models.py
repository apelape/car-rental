from neo4j import GraphDatabase

URI = "neo4j+s://<your-neo4j-instance-uri>"
AUTH = ("neo4j", "<your-password>")


class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(uri, auth=(user, pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


db = Neo4jConnection(URI, AUTH[0], AUTH[1])


class Car:
    def __init__(self, id, make, model, year, location, status):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status

    # Method to find a car by its ID
    @staticmethod
    def find_by_id(car_id):
        car_node = db.query("MATCH (car:Car) WHERE car.id = $id RETURN car", {'id': car_id})
        return Car(**car_node[0]['car']) if car_node else None

    # Methods to create, update, delete car nodes etc. go here


class Customer:
    def __init__(self, id, name, age, address):
        self.id = id
        self.name = name
        self.age = age
        self.address = address

    # Method to find a customer by ID
    @staticmethod
    def find_by_id(customer_id):
        customer_node = db.query("MATCH (customer:Customer) WHERE customer.id = $id RETURN customer",
                                 {'id': customer_id})
        return Customer(**customer_node[0]['customer']) if customer_node else None

    # Methods to create, update, delete customer nodes etc. go here


class Employee:
    def __init__(self, id, name, address, branch):
        self.id = id
        self.name = name
        self.address = address
        self.branch = branch

    # Method to find an employee by ID
    @staticmethod
    def find_by_id(employee_id):
        employee_node = db.query("MATCH (employee:Employee) WHERE employee.id = $id RETURN employee",
                                 {'id': employee_id})
        return Employee(**employee_node[0]['employee']) if employee_node else None

    # Methods to create, update, delete employee nodes etc. go here

# Close the database connection when done
# db.close()
