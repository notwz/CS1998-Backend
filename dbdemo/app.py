import json
from flask import Flask, request
from flask.wrappers import Response
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


def success_response(body, status_code=200):
    return json.dumps(body), status_code


def failure_response(message, status_code=404):
    return json.dumps({"error": message}), status_code


@app.route("/")
@app.route("/tasks/")
def get_tasks():
    return success_response({"tasks": DB.get_tasks()})


@app.route("/tasks/", methods=["POST"])
def create_task():
    body = json.loads(request.data)
    description = body.get("description")
    task_id = DB.create_task(description, False)
    return success_response(DB.get_task_by_id(task_id), 201)


@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = DB.get_task_by_id(task_id)
    pass


@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    pass


@app.route("/tasks/<int:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
