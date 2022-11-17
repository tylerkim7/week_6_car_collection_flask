from flask import Blueprint, request, jsonify
from car_collection.helpers import token_required
from car_collection.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{ 'some' : 'value' }

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    price = request.json['price']
    year = request.json['year']
    acceleration = request.json['facceleration']
    max_speed = request.json['max_speed']
    weight = request.json['weight']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    car = Car(make, model, price, price, year, acceleration, max_speed, weight, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.price = request.json['price']
    car.year = request.json['year']
    car.acceleration = request.json['facceleration']
    car.max_speed = request.json['max_speed']
    car.weight = request.json['weight']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)