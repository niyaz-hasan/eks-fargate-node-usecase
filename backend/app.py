"""
Flask application factory for the Employee-Directory backend
------------------------------------------------------------

Adds
  • Secrets-Manager fetch via IRSA (DB_SECRET_ARN env)
  • Retry loop while waiting for the database
  • JWT via flask-jwt-extended
  • /metrics via prometheus_flask_exporter
  • Optional CORS for the React SPA
"""

import json
import logging
import os
import time

import boto3
from flask import Flask
from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy.exc import OperationalError

from config import Config           # default values (can be overridden below)
from models import db
from routes import api

try:
    from flask_cors import CORS
except ModuleNotFoundError:
    CORS = None

# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #
MAX_RETRIES      = int(os.getenv("DB_CONN_RETRIES", 10))
RETRY_DELAY_SECS = int(os.getenv("DB_CONN_DELAY", 3))


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _load_rds_secret() -> dict:
    """Fetch JSON secret from Secrets Manager and return as dict."""
    secret_arn = os.environ.get("DB_SECRET_ARN")
    region     = os.environ.get("AWS_REGION", "ap-south-1")

    if not secret_arn:
        raise RuntimeError("DB_SECRET_ARN env var not set in backend pod")

    sm = boto3.client("secretsmanager", region_name=region)
    resp = sm.get_secret_value(SecretId=secret_arn)
    return json.loads(resp["SecretString"])


def _build_db_uri(secret: dict) -> str:
    """Return SQLAlchemy URI from secret fields."""
    user     = secret["username"]
    password = secret["password"]
    host     = secret["host"]
    port     = secret.get("port", 3306)
    dbname   = secret["dbname"]

    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"


# --------------------------------------------------------------------------- #
# Application factory
# --------------------------------------------------------------------------- #
def create_app(config_object: object = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # ---------- Inject DB URI from Secrets Manager -------------------------
    try:
        secret = _load_rds_secret()
        app.config["SQLALCHEMY_DATABASE_URI"] = _build_db_uri(secret)
    except Exception as exc:
        logging.critical("Could not load DB secret: %s", exc)
        raise

    # ---------- Extensions --------------------------------------------------
    app.config.setdefault("SQLALCHEMY_ENGINE_OPTIONS", {"pool_pre_ping": True})
    db.init_app(app)
    JWTManager(app)
    PrometheusMetrics(app)  # /metrics

    if CORS:
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ---------- Ensure DB reachable ----------------------------------------
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            with app.app_context():
                db.create_all()
            break  # 🎉 success
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


# Gunicorn entry-point
app = create_app()

if __name__ == "__main__":          # local dev only
    app.run(host="0.0.0.0", port=5000, debug=True)
