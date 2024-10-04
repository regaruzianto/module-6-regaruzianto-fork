from flask import Blueprint, jsonify, request
from db import database

animal_route = Blueprint("animal", __name__, url_prefix="/animal")

last_assigned_id = 2

@animal_route.route("/", methods=["GET"])
def get_animal():
    """
    Get all animals
    ---
    responses:
      200:
        description: Get list of all animals
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: rabbit
              age:
                type: integer
                example: 3
              gender:
                type: string
                example: female
              species:
                type: string
                example: mamals
              special_requirements:
                type: string
                example: Needs medication
      404:
        description: No animals found
    """
    animaldb = database.get("animals")   
    if animaldb is None:
        return jsonify({"message": "Animal not found"}),404
    return jsonify(animaldb),200


@animal_route.route("/<int:keyname>", methods=["GET"])
def get_single_animal(keyname):
    """
    Get a single animal by ID
    ---
    parameters:
      - name: keyname
        in: path
        type: integer
        required: true
        description: ID of the animal to retrieve
    responses:
      200:
        description: A single animal object
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: rabbit
            age:
              type: integer
              example: 3
            gender:
              type: string
              example: female
            species:
              type: string
              example: mamals
            special_requirements:
              type: string
              example: Needs medication
      404:
        description: Animal not found
    """
    animaldb = database.get("animals")
    animal = next((item for item in animaldb if item["id"] == keyname), None)
    if animal is None:
        return jsonify({"message": "Animal not found"}), 404
    return jsonify(animal), 200



@animal_route.route("", methods=["POST"])
def add_animal():
    """
    Add a new animal
    ---
    parameters:
      - in: body
        name: body
        description: JSON object containing animal details
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: rabbit
            age:
              type: integer
              example: 3
            gender:
              type: string
              example: female
            species:
              type: string
              example: mamals
            special_requirements:
              type: string
              example: Needs medication
    responses:
      201:
        description: Animal created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 3
            name:
              type: string
              example: rabbit
            age:
              type: integer
              example: 3
            gender:
              type: string
              example: female
            species:
              type: string
              example: mamals
            special_requirements:
              type: string
              example: Needs medication
      400:
        description: Animal already exists
    """
    global last_assigned_id 

    data = request.json
    name = data.get("name")
    age = data.get("age")
    gender = data.get('gender')
    species = data.get("species")
    special_req = data.get("special requirements")
    animaldb = database.get("animals")
    animal = next((item for item in animaldb if item["name"] == name), None)
    if animal :
        return jsonify({"message": "User already exists"}), 400
    
    last_assigned_id += 1
    new_id = last_assigned_id
    new_animal = {
        "id": new_id,
        "name": name,
        "age": age,
        "gender":gender,
        "species": species,
        "special requirements": special_req
    }
    
    animaldb.append(new_animal)
    
    return jsonify(new_animal), 201



@animal_route.route("/<int:id>", methods=["PUT"])
def update_animal(id):
    """
    Update an existing animal
    ---
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID of the animal to update
      - in: body
        name: body
        description: JSON object containing updated animal details
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: rabbit
            age:
              type: integer
              example: 4
            gender:
              type: string
              example: female
            species:
              type: string
              example: mamals
            special_requirements:
              type: string
              example: Needs medication
    responses:
      200:
        description: Animal updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: rabbit
            age:
              type: integer
              example: 4
            gender:
              type: string
              example: female
            species:
              type: string
              example: mamals
            special_requirements:
              type: string
              example: Needs medication
      404:
        description: Animal not found
    """
    animaldb = database.get("animals")
    data = request.json
    name = data.get("name")
    age = data.get("age")
    gender = data.get('gender')
    species = data.get("species")
    special_req = data.get("special requirements")
    animal = next((item for item in animaldb if item["id"] == id), None)

    if animal is None :
        return jsonify({"message": "animal not found"})
    
    if name:
        animal["name"] = name
    if age:
        animal["age"] = age
    if gender:
        animal["gender"] = gender
    if species:
        animal["species"] = species
    if special_req:
        animal["special requirements"] = special_req

    return jsonify(animal)

    

@animal_route.route("/<int:id>", methods=["DELETE"])
def delete_animal(id):
    """
    Delete an existing animal
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the animal to delete
    responses:
      200:
        description: Animal deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Animal with ID 1 has been deleted successfully."
      404:
        description: Animal not found
    """
    animaldb = database.get("animals")
    
    animal = next((item for item in animaldb if item["id"] == id), None)
    
    if animal is None:
        return jsonify({"message": "Animal not found"}), 404
    
    # Hapus hewan dari database
    animaldb.remove(animal)
    
    return jsonify({"message": f"Animal with ID {id} has been deleted successfully."}), 200