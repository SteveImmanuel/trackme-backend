from flask import Flask
from trackme.api import api_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, load_dotenv=True, port=5000)