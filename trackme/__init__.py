import sentry_sdk
import trackme.blueprints as blueprints
from flask import Flask
from trackme.contants import SENTRY_DSN
from sentry_sdk.integrations.flask import FlaskIntegration

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )

def create_app():
    app = Flask(__name__)
    for bp in blueprints.bp_list:
        app.register_blueprint(bp)

    return app