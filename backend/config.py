# config.py
import os
import boto3
import json
import urllib.parse

def get_rds_secret():
    secret_name = os.getenv("DB_SECRET_NAME")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret['username'], secret['password']

class Config:
    try:
        username, password = get_rds_secret()
    except Exception as e:
        print("Error fetching RDS secret:", e)
        username = "admin"
        password = "password"

    user     = urllib.parse.quote_plus(username)
    password = urllib.parse.quote_plus(password)
    host     = os.getenv("DB_HOST", "localhost")
    port     = os.getenv("DB_PORT", "3306")
    dbname   = os.getenv("DB_NAME", "employees")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")