import argparse
from urllib.parse import quote

from flask import Flask, url_for
from flask import redirect, request, jsonify
import requests

app = Flask(__name__)

# TODO que el client_id y client_secret se pasen como parametros al iniciar / en otro lado
CLIENT_ID = 'p3A4yLY7fJ9dqtSxknlncrCF'
CLIENT_SECRET = 'tJYy8q1cjR4fODaCTEwA8xQIUBmMaLGwCQ0JEjSrxatBelAX'

@app.route('/hello_world')
def hello_world():
    return 'Hello, world!'

@app.route('/login')
def login():
    # TODO: use oauth server to redirect the URI
    return "Here is where I give you a redirect URI but I dont know how to do it yet hah"

# Esta es la PAGINA (no endpoint) a la que se accede y desde donde se inicia. Requiere que antes este cargado el client id y su secreto
# Esto lo llama el user_agent, seria el paso A
@app.route('/test_oauth')
def test_oauth():
    # Primer paso de RFC 6749 punto 4.1 authorization code grant. Aca esta medio cambiado de la RFC 
    # TODO ver porque
    client_id = CLIENT_ID
    # paso A porque mando el client identifier y en el scope esta la redirect_URI
    # En el medio esto pide el consentimiento de parte del owner. Eso es el paso B
    # Una vez dado el consentimiento, devuelve el authorization code a la redirect_URI, que es el paso C 
    # La redirect URI es /receive_code
    return redirect('https://127.0.0.1:5002/oauth/authorize?response_type=code&client_id='+client_id+'&scope=profile')

# Este es el endpoint donde el oauth debe devolver el authorization code con el que se pide el token
@app.route('/receive_code')
def receive_code():
    auth_code = request.args.get('code')
    # Paso D: Con el Auth code se pide el token para acceder al recurso. 
    response_token = requests.post('https://127.0.0.1:5002/oauth/token', auth=(
        CLIENT_ID, # es el client_id
        CLIENT_SECRET, # es el client_secret
        ),data={
        'code' : auth_code,
        'grant_type' : 'authorization_code',
        'scope' : 'profile'}, verify=False) # TODO al arreglar el SSL para el oauth hay que sacar los verify false
    token = response_token.json()['access_token']
    # Nos devolvio el token (paso E). Este lo ponemos en el header y con eso nos devuelve los datos pedidos

    headers = {"Authorization": "Bearer "+ str(token)}

    return requests.get('https://127.0.0.1:5002/api/me',headers=headers, verify=False).text


parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true')
args = parser.parse_args()

app.run(port=5001, debug=args.debug)


