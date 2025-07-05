import os
import urllib.parse
import boto3
from botocore.exceptions import ClientError

class Config:
    @staticmethod
    def get_secret(secret_name, region_name="us-east-1"):
        """Retrieve secret from AWS Secrets Manager"""
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
            raise e

        return eval(get_secret_value_response['SecretString'])

    # If a full DATABASE_URL is supplied (e.g. from Secrets Manager),
    # just use it. Otherwise build one using Secrets Manager or local defaults
    if "DATABASE_URL" in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    else:
        # Try to get credentials from Secrets Manager
        try:
            secret_name = os.getenv("DB_SECRET_NAME")
            if secret_name:
                secret = get_secret(secret_name)
                user = urllib.parse.quote_plus(secret['username'])
                password = urllib.parse.quote_plus(secret['password'])
            else:
                raise ValueError("DB_SECRET_NAME not set")
        except Exception:
            # Fall back to environment variables or defaults
            user = urllib.parse.quote_plus(os.getenv("DB_USER", "admin"))
            password = urllib.parse.quote_plus(os.getenv("DB_PASS", "password"))
        
        host = os.getenv("DB_HOST", "mysql")      # docker-compose service name
        port = os.getenv("DB_PORT", "3306")
        dbname = os.getenv("DB_NAME", "employees")
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")