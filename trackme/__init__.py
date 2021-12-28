from flask import Flask
import trackme.blueprints as blueprints


def create_app():
    app = Flask(__name__)
    for bp in blueprints.bp_list:
        app.register_blueprint(bp)

    return app