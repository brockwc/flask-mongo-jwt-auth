from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/flask-mongo"
app.config["JWT_SECRET_KEY"] = "eat-at-joes"

mongo = PyMongo(app)
