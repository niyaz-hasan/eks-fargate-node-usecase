import os
import json
from flask import Flask
import boto3
from botocore.exceptions import ClientError
import logging
from models import db

def get_db_config():
    """Combine ConfigMap values with Secrets Manager credentials"""
    # Get credentials from Secrets Manager
    secret_name = os.getenv("DB_SECRET_ARN")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logging.error(f"Error retrieving secret: {e}")
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])

    # Get host/port from environment (populated from ConfigMap)
    db_config = {
        'username': secret['username'],
        'password': secret['password'],
        'host': os.getenv("DB_HOST"),
        'port': os.getenv("DB_PORT"),
        'dbname': os.getenv("DB_NAME")
    }
    
    return db_config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure database using combined config
    db_config = get_db_config()
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{db_config['username']}:{db_config['password']}@"
        f"{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    from routes import api_blueprint
    app.register_blueprint(api_blueprint)
    
    return app