# app.py
#from flask import Flask, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from config import Config
#
#app = Flask(__name__)
#app.config.from_object(Config)
#
#db = SQLAlchemy(app)
#
## Register API routes
#from routes import api
#app.register_blueprint(api)
#
## Example model
#class Employee(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String(80))
#    department = db.Column(db.String(80))
#
## Example route
#@app.route("/")
#def health_check():
#    return jsonify({"status": "Backend API is running!"})
#
## WSGI entrypoint for Gunicorn
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000)

# app.py
from flask import Flask, jsonify
from config import Config
from models import db  # Import the db from models.py
from routes import api

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the shared db instance with this Flask app
db.init_app(app)

# Register Blueprint
app.register_blueprint(api)

@app.route("/")
def health_check():
    return jsonify({"status": "Backend API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
