from app import app
from flask import jsonify, request
from bson.json_util import loads
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash

from models import Users

@app.route('/')
def index():
    return jsonify({ 'msg': 'Hello, World!' })

@app.route('/login', methods=['POST'])
def login():
    test = Users.get_one_by_credentials({ 'email': request.json['email'] })
    # test to see if the user exists in the DB (using their email)
    if test:
        # if they do exist, verify their password
        user = loads(test)
        valid_password = check_password_hash(user['password'], request.json['password'])
        if valid_password:
            # if their password is good, create a token and send it back in the response
            access_token = create_access_token(identity=request.json['email'])
            return jsonify({ 'msg': 'All good!', 'access_token': access_token })
        else:
            return jsonify({ 'msg': 'Email or password is incorrect!' })
    else:
        return not_found()

@app.route('/profile')
@jwt_required
def profile():
    return jsonify({ 'msg': "You're free to access your profile" })

@app.route('/users')
def users():
    return Users.get_all()

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return Users.delete_one(user_id)

@app.route('/register', methods=['POST'])
def register():
    _json = request.json
    name = _json['name']
    email = _json['email']
    password = _json['password']

    if name and email and password:
        # signup a user
        return Users.create({
            'name': name,
            'email': email,
            'password': password
        })
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run()
