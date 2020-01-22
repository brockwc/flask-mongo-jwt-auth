from app import app, mongo
from flask import jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from werkzeug.security import generate_password_hash

class Users:
    def create(data):
        hashed_password = generate_password_hash(data['password'])
        mongo.db.user.insert_one({
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password
        })
        resp = jsonify({ 'msg': 'User created successfully' })
        resp.status_code = 200
        return resp

    def get_one_by_credentials(data):
        user = mongo.db.user.find_one({ 'email': data['email'] })
        return dumps(user)

    def get_all():
        users = mongo.db.user.find()
        return dumps(users)

    def delete_one(user_id):
        user = mongo.db.user.find_one({ '_id': ObjectId(user_id) })
        if user:
            mongo.db.user.delete_one({ '_id': ObjectId(user_id) })
            return jsonify({ 'msg': 'User deleted successfully!' })
        else:
            return jsonify({ 'msg': 'A user with that {} could not be found'.format(user_id) })
