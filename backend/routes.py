from flask import request, jsonify
from database import get_connection

def register_routes(app):

    @app.route("/api/admin/login", methods=["POST"])
    def admin_login():
        data = request.get_json()
        
        username = data.get("username")
        password = data.get("password")

        conn = get_connection()
        cursor = conn.cursor()

        # Parameterized query prevents SQL injection
        cursor.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (username, password)
        )
        
        admin = cursor.fetchone()
        conn.close()

        if admin:
            return jsonify({
                "success": True,
                "message": "Login Successful"
            }), 200

        return jsonify({
            "success": False,
            "message": "Invalid Username or Password"
        }), 401


    @app.route("/api/student", methods=["POST"])
    def add_student():
        data = request.get_json()
        
        name = data.get("name")
        roll_no = data.get("roll_no")
        department = data.get("department")
        password = data.get("password")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO students(name, roll_no, department, password)
                VALUES(?, ?, ?, ?)
            """, (name, roll_no, department, password))
            
            conn.commit()

            return jsonify({
                "success": True,
                "message": "Student Added Successfully"
            }), 201

        except Exception as e:
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        finally:
            # Ensures the connection closes even if an error occurs
            conn.close()