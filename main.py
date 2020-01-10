from app import app
from flask import jsonify, request

from models import Users

@app.route('/')
def index():
    return jsonify({ 'msg': 'Hello, World!' })

@app.route('/users')
def users():
    return Users.get_all()

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
