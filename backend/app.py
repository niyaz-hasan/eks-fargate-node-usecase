# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Example model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    department = db.Column(db.String(80))

# Example route
@app.route("/")
def health_check():
    return jsonify({"status": "Backend API is running!"})

# WSGI entrypoint for Gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)