from flask import Blueprint, jsonify, request
from flask import current_app
from functools import wraps
import jwt
import datetime
import json
from models import User

bp = Blueprint('bp', __name__)

def token_verif(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        else:
            return jsonify({'message' : 'No se encontró el Token'}), 403
        
        try:
            public_key = open(current_app.config["PUBLIC_KEY_URI"], 'rb').read()
            data = jwt.decode(token, public_key, algorithms=["RS256"])
            print(data['id'])
        except Exception as e:
            return jsonify({'message' : 'Token inválido'}), 403  
        
        try:
            usersInfoDB = json.loads(open(current_app.config['USERS_DB_URI']).read())
            userDict = next(filter(lambda user : user["id"] == data["id"], usersInfoDB))
        except:
            return jsonify({'message' : 'Usuario no encontrado'}), 404
        user = User(userDict["id"], userDict["nombre"], userDict["is_admin"])

        return f(user, *args, **kwargs)
    return wrapped

@bp.route("/userInfo", methods = ['GET'])
@token_verif
def getUserInfo(user):
    return user.toJSON()

@bp.route("/allUsers", methods = ['GET'])
@token_verif
def getAllUsers(user):
    if not user.is_admin:
        return jsonify({"message" : "El usuario no se encuentra autorizado"}), 403
    usersInfoDB = json.loads(open(current_app.config['USERS_DB_URI']).read())
    return json.dumps(usersInfoDB)

@bp.route("/getToken", methods = ['GET'])
def getToken():
    idUser = int(request.args.get('id'))
    print(idUser)
    private_key = open(current_app.config["PRIVATE_KEY_URI"], 'rb').read()            
    token = jwt.encode({'id' : idUser, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, private_key, algorithm='RS256')
    return jsonify({'token' : token})
