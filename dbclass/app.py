import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)
