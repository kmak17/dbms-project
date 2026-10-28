"""
====================================================================
DBMS PROJECT: HOSTEL ROOM BOOKING SYSTEM
app.py - Main Application Server (Flask + SQLite3)
Run command: python app.py
URL: http://127.0.0.1:5000
====================================================================
"""

import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hostel.db")
SCHEMA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hostel_app.html")


def get_db():
    """Connect to SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Creates database and tables from schema.sql if not exists."""
    if not os.path.exists(DB_FILE):
        conn = get_db()
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()


@app.before_request
def setup():
    init_db()


# --------------------------------------------------------------------
# 1. FRONTEND ROUTE
# --------------------------------------------------------------------
@app.route("/")
def index():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------------
# 2. STUDENT CRUD APIS
# --------------------------------------------------------------------

# READ: Get all students (with optional search)
@app.route("/api/students", methods=["GET"])
def get_students():
    q = request.args.get("q", "").strip()
    conn = get_db()
    cursor = conn.cursor()

    if q:
        search_pattern = f"%{q}%"
        cursor.execute("""
            SELECT s.student_id, s.roll_no, s.name, s.gender, s.department, s.phone, s.room_id,
                   b.block_name, r.room_number
            FROM students s
            LEFT JOIN rooms r ON s.room_id = r.room_id
            LEFT JOIN blocks b ON r.block_id = b.block_id
            WHERE s.roll_no LIKE ? OR s.name LIKE ? OR s.department LIKE ?
            ORDER BY s.student_id DESC
        """, (search_pattern, search_pattern, search_pattern))
    else:
        cursor.execute("""
            SELECT s.student_id, s.roll_no, s.name, s.gender, s.department, s.phone, s.room_id,
                   b.block_name, r.room_number
            FROM students s
            LEFT JOIN rooms r ON s.room_id = r.room_id
            LEFT JOIN blocks b ON r.block_id = b.block_id
            ORDER BY s.student_id DESC
        """)

    students = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(students)


# CREATE: Add a new student
@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json or {}
    roll_no = data.get("roll_no", "").strip()
    name = data.get("name", "").strip()
    gender = data.get("gender", "Male")
    department = data.get("department", "").strip()
    phone = data.get("phone", "").strip()
    room_id = data.get("room_id")

    if not roll_no or not name:
        return jsonify({"success": False, "message": "Roll Number and Name are required."}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Check if roll number already exists
        cursor.execute("SELECT student_id FROM students WHERE roll_no = ?", (roll_no,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": f"Roll Number '{roll_no}' already exists."}), 400

        # Check if room is already occupied
        if room_id:
            cursor.execute("SELECT student_id FROM students WHERE room_id = ?", (room_id,))
            if cursor.fetchone():
                return jsonify({"success": False, "message": "The selected room is already occupied."}), 400

        # Insert new student
        cursor.execute("""
            INSERT INTO students (roll_no, name, gender, department, phone, room_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (roll_no, name, gender, department, phone, room_id))
        conn.commit()
        return jsonify({"success": True, "message": "Student registered successfully."})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()


# READ: Get single student by ID
@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.student_id, s.roll_no, s.name, s.gender, s.department, s.phone, s.room_id,
               b.block_name, r.room_number
        FROM students s
        LEFT JOIN rooms r ON s.room_id = r.room_id
        LEFT JOIN blocks b ON r.block_id = b.block_id
        WHERE s.student_id = ?
    """, (student_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "message": "Student not found."}), 404
    return jsonify(dict(row))


# UPDATE: Update student details & room
@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json or {}
    roll_no = data.get("roll_no", "").strip()
    name = data.get("name", "").strip()
    gender = data.get("gender", "Male")
    department = data.get("department", "").strip()
    phone = data.get("phone", "").strip()
    room_id = data.get("room_id")

    if not roll_no or not name:
        return jsonify({"success": False, "message": "Roll Number and Name are required."}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        # Check duplicate roll number on other students
        cursor.execute("SELECT student_id FROM students WHERE roll_no = ? AND student_id != ?", (roll_no, student_id))
        if cursor.fetchone():
            return jsonify({"success": False, "message": f"Roll Number '{roll_no}' belongs to another student."}), 400

        # Check if room is occupied by another student
        if room_id:
            cursor.execute("SELECT student_id FROM students WHERE room_id = ? AND student_id != ?", (room_id, student_id))
            if cursor.fetchone():
                return jsonify({"success": False, "message": "The selected room is already occupied."}), 400

        cursor.execute("""
            UPDATE students
            SET roll_no = ?, name = ?, gender = ?, department = ?, phone = ?, room_id = ?
            WHERE student_id = ?
        """, (roll_no, name, gender, department, phone, room_id, student_id))
        conn.commit()
        return jsonify({"success": True, "message": "Student updated successfully."})
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()


# DELETE: Delete student
@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Student deleted successfully. Room is now available."})


# --------------------------------------------------------------------
# 3. ROOMS & SUMMARY APIS
# --------------------------------------------------------------------

# Get rooms (for 5-block matrix or available dropdown)
@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    avail_only = request.args.get("available")
    include_room_id = request.args.get("include_room_id", type=int)
    block_id = request.args.get("block_id", type=int)

    conn = get_db()
    cursor = conn.cursor()

    if avail_only:
        # Returns rooms not occupied by any student
        if include_room_id:
            cursor.execute("""
                SELECT r.room_id, b.block_name, r.room_number 
                FROM rooms r
                JOIN blocks b ON r.block_id = b.block_id
                WHERE r.room_id NOT IN (
                    SELECT room_id FROM students WHERE room_id IS NOT NULL AND room_id != ?
                )
                ORDER BY b.block_id, r.room_number
            """, (include_room_id,))
        else:
            cursor.execute("""
                SELECT r.room_id, b.block_name, r.room_number 
                FROM rooms r
                JOIN blocks b ON r.block_id = b.block_id
                WHERE r.room_id NOT IN (
                    SELECT room_id FROM students WHERE room_id IS NOT NULL
                )
                ORDER BY b.block_id, r.room_number
            """)
    else:
        # Returns rooms with occupant details
        cursor.execute("""
            SELECT r.room_id, b.block_id, b.block_name, r.room_number,
                   s.student_id, s.roll_no, s.name AS student_name,
                   CASE WHEN s.student_id IS NOT NULL THEN 'Occupied' ELSE 'Available' END AS status
            FROM rooms r
            JOIN blocks b ON r.block_id = b.block_id
            LEFT JOIN students s ON r.room_id = s.room_id
            WHERE (? IS NULL OR r.block_id = ?)
            ORDER BY r.block_id, r.room_id
        """, (block_id, block_id))

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)


# Get summary counts
@app.route("/api/summary", methods=["GET"])
def get_summary():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM rooms")
    total_rooms = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE room_id IS NOT NULL")
    occupied_rooms = cursor.fetchone()[0]

    available_rooms = total_rooms - occupied_rooms
    conn.close()

    return jsonify({
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "available_rooms": available_rooms
    })


if __name__ == "__main__":
    print("[SERVER] Hostel Room Booking System is running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
