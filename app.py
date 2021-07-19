# python3
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)

# Correctly locate base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy Database - Correctly locate database file in the path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Init ma 
ma = Marshmallow(app)


# Customer Class/Model
class Customer(db.Model):
    # Assign database fields
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.Integer)

    # Initialize fields to self
    def __init__(self, first_name, last_name, email, address, city, state, zip_code):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code


# Customer Schema
class CustomerSchema(ma.Schema):
    class Meta:
        # fields that are allowed to be shown
        fields = ('id','first_name','last_name','email','address','city','state','zip_code') 

# Init Schema 
customer_schema = CustomerSchema()


# Create a Customer
@app.route('/customers', methods=['POST'])
def add_customer():

    # fetch data passed from request - using postman/swagger 
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    zip_code = request.json['zip_code']

    # variable instantiated to the Customer class, passing the fields in
    new_customer = Customer(first_name, last_name, email, address, city, state, zip_code)

    # add and commit the new customer to the database
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 200


# Query all customers or customers by city
@app.route('/customers', methods=['GET'])
def query_city():
    try:
        # Get city from the url query 
        query_params = request.args.to_dict(flat=False)
        city = query_params['city']
        customer_city = city[0]

        # pass the customer_city to the database and return the filtered results
        db = Customer.query.filter_by(city=customer_city).all()
        result = customer_schema.dump(db,many=True)
        if not result:
            abort(404, "City not found")
        return jsonify(result), 200

        # KeyError occurs due to the required order of execution, so I catch the exception
    except KeyError as err:
        print(f"Caught Exception -> Key Error: {err}, continuing execution")

        # query and return all customers
        all_customers = Customer.query.all()
        result = customer_schema.dump(all_customers,many=True)
        if not result:
            abort(404, "No Customers in database")
        return jsonify({"All Customers":result}), 200



# Get Single Customers by ID
@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        abort(404, 'Customer ID does not exist')
    return customer_schema.jsonify(customer), 200


# Update Customer Information by ID
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        abort(404, 'Customer cannot be updated, ID does not exist')

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    zip_code = request.json['zip_code']

    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.address = address
    customer.city = city
    customer.state = state
    customer.zip_code = zip_code

    db.session.commit()

    return customer_schema.jsonify(customer), 200


# Delete Customer from database
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        abort(404, 'Customer ID does not exist')

    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer), 200


# Run Server
if __name__ == '__main__':
    app.run(debug=True) # False in prod
