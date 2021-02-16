from flask import Blueprint, jsonify, request
from flask import current_app
from functools import wraps
import jwt
import json
from models import User
import traceback

bp = Blueprint('bp', __name__)


def token_verif(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        
        if 'Authorization' in request.headers:
            bearer_token = request.headers['Authorization']
            token = bearer_token.split(" ")[1]
        else:
            return jsonify({'message': 'token required'}), 403
        
        try:
            public_key = open(current_app.config['PUBLIC_KEY_PATH'], 'rb').read()
            jwt_data = jwt.decode(token, public_key, algorithms=["RS256"])
        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': 'invalid token'}), 403
        
        try:
            users_pets_db = json.loads(open(current_app.config['USERS_DB_URI']).read())
            user_dict = next(filter(lambda user: user["user_id"] == jwt_data["user"]["user_id"], users_pets_db))
        except Exception:
            traceback.print_exc()
            return jsonify({'message': 'user not found'}), 404

        user = User(user_dict["user_id"], user_dict["nickname"],
                    jwt_data["user"]["is_admin"], user_dict["pets"])

        return f(user, *args, **kwargs)
    return wrapped


@bp.route("/my_info", methods=['GET'])
@token_verif
def get_user_info(user):
    return user.to_json()


@bp.route("/all_users", methods=['GET'])
@token_verif
def get_all_users(user):
    if not user.is_admin:
        return jsonify({"message": "not authorized"}), 403
    users_info_db = json.loads(open(current_app.config['USERS_DB_URI']).read())

    return json.dumps(users_info_db)
