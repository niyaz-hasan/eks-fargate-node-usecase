from flask import Flask
from flask_cors import CORS
from models import db
from config import Config
from routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app) 
    
    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)