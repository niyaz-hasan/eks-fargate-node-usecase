import os
import json
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = os.environ.get("SECRET_NAME")
    region_name = os.environ.get("AWS_REGION")

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
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            # Handle binary secret if needed
            pass

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')
    
    # Get DB credentials from Secrets Manager
    db_credentials = get_secret()
    db_user = db_credentials['username']
    db_password = db_credentials['password']
    db_host = db_credentials['host']
    db_port = db_credentials['port']
    db_name = db_credentials['dbname']

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False