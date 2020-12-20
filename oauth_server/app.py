import argparse
from urllib.parse import quote

from flask import Flask, url_for
from flask import redirect, request, jsonify
import requests

app = Flask(__name__)

@app.route('/oauth/authorize')
def authorize():
    client_id = request.args.get('client_id')
    scope = request.args.get('scope')
    return "aa"

@app.route('/oauth/token')
def token():
    return "Not implemented"


parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true')
args = parser.parse_args()

app.run(port=5001, debug=args.debug)


