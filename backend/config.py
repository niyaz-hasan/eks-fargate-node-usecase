import os, urllib.parse

class Config:
    # DB URL (local docker-compose or injected by Secrets Manager)
    if "DATABASE_URL" in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    else:
        user = urllib.parse.quote_plus(os.getenv("DB_USER", "admin"))
        pwd  = urllib.parse.quote_plus(os.getenv("DB_PASS", "password"))
        host = os.getenv("DB_HOST", "mysql")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "employees")
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY        = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY    = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")  # ← new
    CORS_ORIGINS      = os.getenv("CORS_ORIGINS", "*")
