from flask import Flask, url_for

app = Flask(__name__)

@app.route('/hello_world')
def hello_world():
    return 'Hello, world!'

@app.route('/login')
def login():
    # TODO: use oauth server to redirect the URI
    return "Here is where I give you a redirect URI but I dont know how to do it yet hah"

app.run(debug=True)


