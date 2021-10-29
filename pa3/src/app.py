from datetime import datetime
import json

import db
from flask import Flask
from flask import request

DB = db.DatabaseDriver()

app = Flask(__name__)


def success_response(body, code=200):
    return json.dumps(body), code


def failure_response(body, code=404):
    return json.dumps(body), code


@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here


@app.route("/api/users/")
def get_all_users():


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
