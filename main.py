import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/users", methods=["GET"])
def get_users():
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return jsonify({"message": "No users found"}), 404

    if not users:
        return jsonify({"message": "No users found"}), 204

    return jsonify(users)


@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        return jsonify({"message": "No users found"}), 404

    for user in users:
        if user["id"] == int(id):
            return jsonify(user)

    return jsonify({"message": "User with ID {} not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"message": "Invalid JSON payload"}), 400

    user = {
        "id": int(data["id"]),
        "name": data["name"],
        "age": int(data["age"]),
        "email": data["email"],
    }

    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    for existing_user in users:
        if existing_user["id"] == user["id"]:
            return jsonify({"message": "User with ID {} already exists"}), 409

    users.append(user)

    with open("users.json", "w") as f:
        json.dump(users, f)

    return jsonify({"message": "User created"}), 201


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"message": "Invalid JSON payload"}), 400

    user = {
        "id": int(data["id"]),
        "name": data["name"],
        "age": int(data["age"]),
        "email": data["email"],
    }

    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    user_found = False
    for i, u in enumerate(users):
        if u["id"] == int(id):  # Convert 'id' to an integer
            users[i] = user
            user_found = True
            break

    if not user_found:
        return jsonify({"message": "User with ID {} not found"}), 404

    with open("users.json", "w") as f:
        json.dump(users, f)

    return jsonify({"message": "User updated"})



@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    user_found = False
    for i, u in enumerate(users):
        if u["id"] == int(id):
            users.pop(i)
            user_found = True
            break

    if not user_found:
        return jsonify({"message": "User with ID {} not found"}), 404

    with open("users.json", "w") as f:
        json.dump(users, f)

    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
