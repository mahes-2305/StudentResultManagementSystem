from flask import Flask, jsonify
from flask_cors import CORS

from database import create_tables
from routes import register_routes

app = Flask(__name__)

CORS(app)

create_tables()

register_routes(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student Result Management System API",
        "status": "Running"
    })


if __name__ == "__main__":
    app.run(debug=True)
