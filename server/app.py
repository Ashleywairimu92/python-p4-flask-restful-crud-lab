#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# GET route: Retrieve plant by ID
@app.route('/plants/<int:id>', methods=['GET'])
def get_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        abort(404, description="Plant not found")
    return jsonify(plant.to_dict()), 200

# PATCH route: Update "is_in_stock" field for a plant by ID
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        abort(404, description="Plant not found")
    
    data = request.get_json()
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']
        db.session.commit()
    
    return jsonify(plant.to_dict()), 200

# DELETE route: Delete a plant by ID
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get(id)
    if not plant:
        abort(404, description="Plant not found")
    
    db.session.delete(plant)
    db.session.commit()
    
    return '', 204  # Return no content after successful deletion

 
if __name__ == '__main__':
    app.run(port=5555, debug=True)
