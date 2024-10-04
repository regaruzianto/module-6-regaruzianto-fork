from flask import Blueprint, jsonify, request
from db import database

user_route = Blueprint("user", __name__, url_prefix="/user")

last_assigned_id = 2

@user_route.route("/", methods=["GET"])
def get_user():
  """
    Get all user
    ---
    responses:
      200:
        description: get list all user
    """
  userdb = database.get("users")   
  if userdb is None:
      return jsonify({"message": "user not found"}),404
  return jsonify(userdb),200


@user_route.route("/<int:keyname>", methods=["GET"])
def get_single_user(keyname):
  """
    Get a single user by ID
    ---
    parameters:
      - name: keyname
        in: path
        type: integer
        required: true
        description: ID of the user to retrieve
    responses:
      200:
        description: A single user object
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john.doe@example.com
            phone number:
              type: integer
              example: 1234567
            role:
              type: string
              example: manager
            schedule:
              type: string
              example: monday-friday, 07.00-17.00
      404:
        description: User not found
    """
  userdb = database.get("users")
  user = next((item for item in userdb if item["id"] == keyname), None)
  if user is None:
      return jsonify({"message": "user not found"}), 404
  return jsonify(user), 200



@user_route.route("", methods=["POST"])
def add_user():
  """
    Add a new user
    ---
    parameters:
      - in: body
        name: body
        description: JSON object containing user details
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: John
            email:
              type: string
              example: john@example.com
            phone number:
              type: string
              example: 08123456789
            role:
              type: string
              example: Admin
            schedule:
              type: string
              example: Monday-Friday, 9AM-5PM
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: John
            email:
              type: string
              example: john@example.com
            phone number:
              type: string
              example: 08123456789
            role:
              type: string
              example: Admin
            schedule:
              type: string
              example: Monday-Friday, 9AM-5PM
      400:
        description: User already exists
    """
  global last_assigned_id 
  data = request.json
  name = data.get("name")
  email = data.get("email")
  phone_num = data.get("phone number")
  role = data.get("role")
  schedule = data.get("schedule")
  userdb = database.get("users")
  user = next((item for item in userdb if item["name"] == name), None)
  if user :
      return jsonify({"message": "User already exists"}), 400
  
  last_assigned_id += 1
  new_id = last_assigned_id
  new_user = {
      "id": new_id,
      "name": name,
      "email": email,
      "phone number":phone_num,
      "role": role,
      "schedule": schedule,
  }
  
  userdb.append(new_user)
  
  return jsonify(new_user), 201




@user_route.route("/<int:id>", methods=["PUT"])
def update_user(id):
  """
  Update an existing user by ID
  ---
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID of the user to update
    - in: body
      name: body
      description: JSON object containing updated user details
      required: true
      schema:
        type: object
        properties:
          name:
            type: string
            example: John
          email:
            type: string
            example: john@example.com
          phone number:
            type: string
            example: 08123456789
          role:
            type: string
            example: Admin
          schedule:
            type: string
            example: Monday-Friday, 9AM-5PM
  responses:
    200:
      description: User updated successfully
      schema:
        type: object
        properties:
          id:
            type: integer
            example: 1
          name:
            type: string
            example: John
          email:
            type: string
            example: john@example.com
          phone number:
            type: string
            example: 08123456789
          role:
            type: string
            example: Admin
          schedule:
            type: string
            example: Monday-Friday, 9AM-5PM
    404:
      description: User not found
  """
  data = request.json
  name = data.get("name")
  email = data.get("email")
  phone_num = data.get("phone number")
  role = data.get("role")
  schedule = data.get("schedule")
  userdb = database.get("users")
  user = next((item for item in userdb if item["id"] == id), None)
  if user is None :
      return jsonify({"message": "user not found"})
  
  if name:
      user["name"] = name
  if email:
      user["email"] = email
  if phone_num:
      user["phone number"] = phone_num
  if role:
      user["role"] = role
  if schedule:
      user["schedule"] = schedule
  return jsonify(user)

    

@user_route.route("/<int:id>", methods=["DELETE"])
def delete_user(id):
  """
  Delete a user by ID
  ---
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID of the user to delete
  responses:
    200:
      description: User deleted successfully
      schema:
        type: object
        properties:
          message:
            type: string
            example: user with ID 1 has been deleted successfully.
    404:
      description: User not found
  """
  userdb = database.get("users")
  
  user = next((item for item in userdb if item["id"] == id), None)
  
  if user is None:
      return jsonify({"message": "user not found"}), 404
  
  userdb.remove(user)
  
  return jsonify({"message": f"user with ID {id} has been deleted successfully."}), 200