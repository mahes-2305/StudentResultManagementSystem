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

    @app.route("/api/student/login", methods=["POST"])
    def student_login():

        data = request.get_json()

        roll_no = data.get("roll_no")
        password = data.get("password")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE roll_no=? AND password=?
        """, (roll_no, password))

        student = cursor.fetchone()

        conn.close()

        if student:

            return jsonify({
                "success": True,
                "student": {
                    "id": student["id"],
                    "name": student["name"],
                    "roll_no": student["roll_no"],
                    "department": student["department"]
                }
            }), 200

        return jsonify({
            "success": False,
            "message": "Invalid Roll Number or Password"
        }), 401        
    
    @app.route("/api/marks", methods=["POST"])
    def add_marks():

        data = request.get_json()

        roll_no = data.get("roll_no")
        subject = data.get("subject")
        marks = data.get("marks")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM students WHERE roll_no=?",
            (roll_no,)
        )

        student = cursor.fetchone()

        if not student:
            conn.close()
            return jsonify({
                "success": False,
                "message": "Student not found"
            }), 404

        cursor.execute("""
        INSERT INTO marks(student_id,subject,marks)
        VALUES(?,?,?)
        """, (student["id"], subject, marks))

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Marks Added Successfully"
        }), 201
    
    @app.route("/api/marks", methods=["PUT"])
    def update_marks():

        data = request.get_json()

        roll_no = data.get("roll_no")
        subject = data.get("subject")
        marks = data.get("marks")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM students WHERE roll_no=?",
            (roll_no,)
        )

        student = cursor.fetchone()

        if not student:
            conn.close()
            return jsonify({
                "success": False,
                "message": "Student not found"
            }), 404

        cursor.execute("""
        UPDATE marks
        SET marks=?
        WHERE student_id=? AND subject=?
        """, (marks, student["id"], subject))

        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({
                "success": False,
                "message": "Subject not found"
            }), 404

        conn.close()

        return jsonify({
            "success": True,
            "message": "Marks Updated Successfully"
        }), 200
    
    @app.route("/api/result/<roll_no>", methods=["GET"])
    def view_result(roll_no):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM students
        WHERE roll_no=?
        """, (roll_no,))

        student = cursor.fetchone()

        if not student:
            conn.close()
            return jsonify({
                "success": False,
                "message": "Student not found"
            }), 404

        cursor.execute("""
        SELECT subject, marks
        FROM marks
        WHERE student_id=?
        """, (student["id"],))

        results = cursor.fetchall()

        result_list = []

        total = 0

        for row in results:

            result_list.append({
                "subject": row["subject"],
                "marks": row["marks"]
            })

            total += row["marks"]

        if len(result_list) > 0:
            percentage = total / len(result_list)
        else:
            percentage = 0

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        else:
            grade = "F"

        conn.close()

        return jsonify({
            "success": True,
            "student": {
                "name": student["name"],
                "roll_no": student["roll_no"],
                "department": student["department"]
            },
            "results": result_list,
            "total": total,
            "percentage": percentage,
            "grade": grade
        })