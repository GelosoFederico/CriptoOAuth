from flask import Blueprint, jsonify, request
from flask import current_app
from functools import wraps
import jwt
import os
import json
from models import User
import traceback

bp = Blueprint('bp', __name__)
home = os.path.expanduser('~')
cripto_config = os.path.join(home, '.cripto-tp')
CLIENT_CONFIG_PATH = os.path.join(cripto_config, 'client_keys.json')

# To decode JWT

def token_verif(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        
        if 'Authorization' in request.headers:
            bearer_token = request.headers['Authorization']
            token = bearer_token.split(" ")[1]
        else:
            return jsonify({'message' : 'token required'}), 403
        
        try:
            public_key = open(current_app.config['PUBLIC_KEY_PATH'], 'rb').read()
            data = jwt.decode(token, public_key, algorithms=["RS256"])
        except Exception as e:
            traceback.print_exc()
            return jsonify({'message' : 'invalid token'}), 403
        
        try:
            usersInfoDB = json.loads(open(current_app.config['USERS_DB_URI']).read())
            userDict = next(filter(lambda user : user["user_id"] == data["user_id"], usersInfoDB))
        except:
            traceback.print_exc()
            return jsonify({'message' : 'user not found'}), 404
        user = User(userDict["user_id"], userDict["name"], userDict["is_admin"])

        return f(user, *args, **kwargs)
    return wrapped

@bp.route("/user_info", methods = ['GET'])
@token_verif
def getUserInfo(user):
    return user.toJSON()

@bp.route("/all_users", methods = ['GET'])
@token_verif
def getAllUsers(user):
    if not user.is_admin:
        return jsonify({"message" : "not authorized"}), 403
    usersInfoDB = json.loads(open(current_app.config['USERS_DB_URI']).read())
    return json.dumps(usersInfoDB)
