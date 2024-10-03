from flask import Blueprint, jsonify, request
from db import database

user_route = Blueprint("user", __name__, url_prefix="/user")

last_assigned_id = 2

@user_route.route("/", methods=["GET"])
def get_user():
    userdb = database.get("users")   
    if userdb is None:
        return jsonify({"message": "user not found"}),404
    return jsonify(userdb),200


@user_route.route("/<int:keyname>", methods=["GET"])
def get_single_user(keyname):
    userdb = database.get("users")
    user = next((item for item in userdb if item["id"] == keyname), None)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    return jsonify(user), 200



@user_route.route("", methods=["POST"])
def add_user():
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
    userdb = database.get("users")
    
    user = next((item for item in userdb if item["id"] == id), None)
    
    if user is None:
        return jsonify({"message": "user not found"}), 404
    
    # Hapus hewan dari database
    userdb.remove(user)
    
    return jsonify({"message": f"user with ID {id} has been deleted successfully."}), 200