from flask import Flask, Blueprint
from server.routes import bp

def createApp(config_object='settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(bp)
    return app




