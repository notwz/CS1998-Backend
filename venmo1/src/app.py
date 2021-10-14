import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


def success_response(body, code=200):
    return json.dumps(body), code


def failure_response(message, code=404):
    return json.dumps({'error': message}), code


@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here

# Get All Users


@app.route("/api/users/")
def get_users():
    return success_response(DB.get_all_users_secure())

# Post a User


@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body["name"]
    username = body["username"]
    balance = body.get("balance", 0)
    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("Something went wrong while creating new user.", 500)
    return success_response(user, 201)

# Retrieve a User


@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found!")
    return success_response(user)

# Delete a User


@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found!")
    DB.delete_user_by_id(user_id)
    return success_response(user)


@app.route("/api/send/", methods=["POST"])
def transfer():
    body = json.loads(request.data)
    sender_id = body["sender_id"]
    receiver_id = body["receiver_id"]
    amount = body["amount"]
    if (sender_id == None or receiver_id == None or amount == None):
        return failure_response("Please input values for each field", 400)
    sender_balance_field = DB.get_sender_balance(sender_id)
    if (sender_balance_field["balance"] < amount):
        return failure_response("Insufficient Funds", 400)

    DB.send_money(sender_id, receiver_id, amount)
    return success_response(body)


@app.route("/test/")
def test():
    a = DB.get_sender_balance(6)
    print(a["balance"])
    res = {
        "a": a,
        "a value": a.get("balance"),
        "a key": a["balance"]}
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
