from flask import Flask, jsonify
from database import create_tables

app = Flask(__name__)

# Create database tables when the application starts
create_tables()

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Student Result Management System API",
        "status": "Running"
    })

if __name__ == "__main__":
    app.run(debug=True)
