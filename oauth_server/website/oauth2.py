import datetime

import jwt
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.integrations.sqla_oauth2 import create_query_client_func
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7636 import CodeChallenge

from .models import db, User
from .models import OAuth2Client, OAuth2AuthorizationCode

OAUTH_PRIVATE_KEY_PATH = 'oauth_server/jwt_keys/ssh-key'

def gen_access_token(client, grant_type, user, scope):
    payload = {
        'iss': 'http://127.0.0.1:5002/oauth/token',
        'sub': 'test client',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'user':  dict(user_id=user.id, username=user.username,
                      is_admin=user.is_admin),
        'scope': scope,
        'grant_type': grant_type,
        'client_id': client.client_id
    }
    private_key = open(OAUTH_PRIVATE_KEY_PATH, 'rb').read()
    s = jwt.encode(payload, private_key, algorithm='RS256')
    return s

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none',
    ]

    def save_authorization_code(self, code, request):
        code_challenge = request.data.get('code_challenge')
        code_challenge_method = request.data.get('code_challenge_method')
        auth_code = OAuth2AuthorizationCode(
            code=code,
            client_id=request.client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )
        db.session.add(auth_code)
        db.session.commit()
        return auth_code

    def query_authorization_code(self, code, client):
        auth_code = OAuth2AuthorizationCode.query.filter_by(
            code=code, client_id=client.client_id).first()
        if auth_code and not auth_code.is_expired():
            return auth_code

    def delete_authorization_code(self, authorization_code):
        db.session.delete(authorization_code)
        db.session.commit()

    def authenticate_user(self, authorization_code):
        return User.query.get(authorization_code.user_id)

def do_not_save(token, request):
    pass

query_client = create_query_client_func(db.session, OAuth2Client)

authorization = AuthorizationServer(
    query_client=query_client,
    save_token=do_not_save, # Because of JWT
)

def config_oauth(app):
    app.config['OAUTH2_ACCESS_TOKEN_GENERATOR'] = gen_access_token
    authorization.init_app(app)
    authorization.register_grant(AuthorizationCodeGrant, [CodeChallenge(required=True)])