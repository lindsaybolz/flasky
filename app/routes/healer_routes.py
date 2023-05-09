from app import db
from app.models.healer import Healer
from app.models.crystal import Crystal
from app.routes.crystal_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

healer_bp = Blueprint("healers", __name__, url_prefix="/healers")

# HEALER ROUTES
@healer_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_healer():
    request_body = request.get_json()
    
    new_healer = Healer(
        name=request_body["name"]
    )
    
    db.session.add(new_healer)
    db.session.commit()
    
    return jsonify(f"Yayyyy Healer {new_healer.name} successfully created!"), 201


@healer_bp.route("", methods=["GET"])
def read_all_healers():
    
    healers = Healer.query.all()
        
    healers_response = []
    
    for healer in healers:
        healers_response.append({ "name": healer.name, "id": healer.id})
    
    return jsonify(healers_response)


@healer_bp.route("/<healer_id>/crystals", methods=['POST'])
def create_crystal_by_id(healer_id):
    healer = validate_model(Healer, healer_id)
    request_body = request.get_json()
    new_crystal = Crystal(
        name=request_body['name'],
        powers=request_body['powers'],
        color=request_body['color'],
        healer=healer)

    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f"Crystal {new_crystal.name} owned by {new_crystal.healer.name} was successfully created"), 201


@healer_bp.route("/<healer_id>/crystals", methods=["GET"])
def get_all_crystals_from_healer(healer_id):
    healer = validate_model(Healer, healer_id)
    crystals_response = []

    for crystal in healer.crystals:
        crystals_response.append(crystal.to_dict())

    return jsonify(crystals_response), 200