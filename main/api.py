import os
from flask import Flask, abort, request, jsonify, g
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
import json
from main import find_path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aplikacja imitujaca jakdojade'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=30):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None  # expired token
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/gettoken')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(30)
    return jsonify({'token': token.decode('ascii'), 'duration': 30}), 201


@app.route('/register', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(409)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201


@app.route('/stops', methods=['GET'])
@auth.login_required
def stops():
    with open('solvro_city.json') as f:
        data = json.load(f)['nodes']
        return json.dumps(data), 200


@app.route('/path', methods=['POST'])
@auth.login_required
def get_resource():
    try:
        result, distance, status = find_path.dijkstra(request.get_json('data')['source'], request.get_json('data')['target'])
    except KeyError:
        return jsonify({'nodes': None, 'distance': None, 'status': {3: "Key error"}}), 400
    return jsonify({'nodes': result, 'distance': distance, 'status': status}, 200)


if __name__ == '__main__':
    if not os.path.exists('main/db.sqlite'):
        db.create_all()
    app.run(debug=True)
