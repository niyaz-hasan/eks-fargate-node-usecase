"""
Flask application factory for the Employee-Directory backend
------------------------------------------------------------

Adds
  • Retry loop while waiting for the database
  • JWT support via flask-jwt-extended
  • Prometheus /metrics endpoint
  • Optional CORS for the React SPA
"""

import logging
import os
import time

from flask import Flask
from sqlalchemy.exc import OperationalError

from config import Config
from models import db
from routes import api

from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import PrometheusMetrics
try:
    from flask_cors import CORS
except ModuleNotFoundError:
    CORS = None

MAX_RETRIES      = int(os.getenv("DB_CONN_RETRIES", 10))
RETRY_DELAY_SECS = int(os.getenv("DB_CONN_DELAY", 3))


def create_app(config_object: object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # ---------- Extensions --------------------------------------------------
    app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {"pool_pre_ping": True})
    db.init_app(app)
    JWTManager(app)
    PrometheusMetrics(app)  # exposes /metrics

    if CORS:
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ---------- Ensure DB is reachable -------------------------------------
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            with app.app_context():
                db.create_all()
            break
        except OperationalError as exc:
            attempts += 1
            logging.warning(
                "Database not ready (%s). Retry %s/%s in %s s …",
                exc.orig, attempts, MAX_RETRIES, RETRY_DELAY_SECS,
            )
            time.sleep(RETRY_DELAY_SECS)
    else:
        logging.critical("Giving up: DB unreachable after retries.")
        raise

    # ---------- Blueprints --------------------------------------------------
    app.register_blueprint(api)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
