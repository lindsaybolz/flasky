from app import db
from app.models.crystal import Crystal
from flask import Blueprint, jsonify, abort, make_response, request

crystal_bp = Blueprint("crystals", __name__, url_prefix="/crystals")
# Helper Function
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

# CRYSTAL Routes
# Create a crystal 
@crystal_bp.route("", methods=['POST'])
def handle_crystal():
    request_body = request.get_json()
    new_crystal = Crystal.from_dict(request_body)

    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f"Crystal {new_crystal.name} successfully created."), 201

# Get all crystals or all crystals with a query param
@crystal_bp.route("", methods=["GET"])
def get_all_crystals():

    color_query = request.args.get('color')
    powers_query = request.args.get('powers')

    if color_query and powers_query:
        crystals = Crystal.query.filter_by(color=color_query, powers=powers_query)
    elif color_query:
        crystals = Crystal.query.filter_by(color=color_query)
    elif powers_query:
        crystals = Crystal.query.filter_by(powers=powers_query)
    else:
        crystals = Crystal.query.all()
    response_body = []
    for crystal in crystals:
        response_body.append(crystal.to_dict())
    
    return jsonify(response_body), 200

# define a route for getting a single crystal
@crystal_bp.route("/<crystal_id>", methods=["GET"])
def read_one_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)
    return crystal.to_dict(), 200

# route for updating a crystal with name, powers, and color
@crystal_bp.route('/<crystal_id>', methods=['PUT'])
def update_crystal(crystal_id):
    crystal =  validate_model(Crystal, crystal_id)
    request_body = request.get_json()

    crystal.name = request_body['name']
    crystal.powers = request_body['powers']
    crystal.color = request_body['color']

    db.session.commit()

    return {'message': f"Crystal {crystal_id} successfully updated."}, 200

# route for deleting a crystal with an id
@crystal_bp.route("/<crystal_id>", methods=['DELETE'])
def delete_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"Crystal {crystal_id} successfully deleted.")

