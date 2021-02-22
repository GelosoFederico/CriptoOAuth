import os
import json
import requests

from flask import Flask
from flask import redirect, request

app = Flask(__name__)

home = os.path.expanduser('~')
cripto_config = os.path.join(home, '.cripto-tp')
CLIENT_CONFIG_PATH = os.path.join(cripto_config, 'client_keys.json')


def get_client_keys():
    if not os.path.exists(CLIENT_CONFIG_PATH):
        raise Exception("Client keys file not found ({})".format(CLIENT_CONFIG_PATH))

    with open(CLIENT_CONFIG_PATH) as json_file:
        data = json.load(json_file)

    return data["client_id"], data["client_secret"]


@app.route('/hello_world')
def hello_world():
    return 'Hello, world!'


@app.route('/test_oauth')
def test_oauth():
    """
    Este es el endpoint al que se debe acceder desde un web browser
    y desde donde se inicia el flujo de autorizacion.
    Requiere que antes esten almacenados el Client ID y Secret en
    el archivo <home>/.cripto-tp/client_keys.json

    Esto lo llama el user_agent, seria el paso A.
    """

    # Primer paso de RFC 6749 punto 4.1 authorization code grant.
    client_id, _ = get_client_keys()

    # paso A porque mando el client identifier y en el scope esta la redirect_URI
    # En el medio esto pide el consentimiento de parte del owner. Eso es el paso B.
    # Una vez dado el consentimiento, devuelve el authorization code a la redirect_URI, que es el paso C 
    # La redirect URI es /receive_code
    return redirect('https://127.0.0.1:5002/oauth/authorize?response_type=code&client_id='+client_id+'&scope=profile')


@app.route('/receive_code')
def receive_code():
    auth_code = request.args.get('code')
    client_id, client_secret = get_client_keys()

    # Paso D: Con el Auth code se pide el token para acceder al recurso.
    response_token = requests.post('https://127.0.0.1:5002/oauth/token',
                                   auth=(client_id, client_secret),
                                   data={'code': auth_code,
                                         'grant_type': 'authorization_code',
                                         'scope': 'profile'},
                                   verify=False)
    json_data = response_token.json()
    token = json_data['access_token']

    # Nos devolvio el token (paso E). Este lo ponemos en el header
    # y con eso nos devuelve los datos pedidos
    print("Token is:", token)

    # Hacemos el request al server del recurso protegido.
    headers = {"Authorization": "Bearer " + str(token)}
    user_info = requests.get('https://127.0.0.1:5003/my_info', headers=headers, verify=False)
    user_info = user_info.json()
    all_users_info = requests.get('https://127.0.0.1:5003/all_users', headers=headers, verify=False)
    all_users_info = all_users_info.json()

    # Integramos la informacion
    total_info = {"user_info": user_info,
                  "all_users": all_users_info}

    return total_info
