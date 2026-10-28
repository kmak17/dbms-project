# Hostel Room Booking System (DBMS Project)

**A.D. Patel Institute of Technology (ADIT) | Academic Year 2026–2027**  
**Subject:** Database Management System (DBMS)  
**Topic:** Hostel Room Booking System (Basic CRUD)  

---

## 1. Overview

This project is a simple, basic **Hostel Room Booking System** built with **Python (Flask)**, **SQLite3**, and a **Plain White UI**.

* **Student CRUD**: Create, Read, Update, and Delete student records.
* **5 Blocks with 20 Rooms Each**: Total of 100 rooms (Block A to Block E).
* **Room Allocation**: Assign rooms to students, change rooms, or vacate rooms.
* **No Sample Data**: The student table starts completely empty so you can enter your own data.
* **No Payment System**: Focused purely on student room booking.

---

## 2. Project Files (Only 4 Files)

```text
DBMS PROject/
├── app.py            # Main application server (Runs backend and database)
├── hostel_app.html   # Plain white user interface (Web page)
├── schema.sql        # Creates tables (Blocks, Rooms, Students) and 100 rooms
├── queries.sql       # SQL queries demonstrating CRUD operations
└── README.md         # Instructions
```

---

## 3. How to Run

1. Open your terminal / command prompt in this folder.
2. Run this single command:
   ```powershell
   python app.py
   ```
3. Open your browser and go to:
   ```text
   http://127.0.0.1:5000
   ```

---

## 4. Features & Usage

* **Add Student (Create)**: Click **"+ Add Student"**, fill in the Roll Number, Name, Department, and pick an available room.
* **View Students (Read)**: See all registered students and their room allocations in a clean table with a search bar.
* **Edit Student (Update)**: Click **"Edit"** on any student to change their phone, name, or room.
* **Delete Student (Delete)**: Click **"Delete"** to remove a student. Their room will automatically become available again.
* **5 Blocks & Rooms Matrix**: Switch to the **"5 Blocks & Rooms Matrix"** tab to check which rooms are vacant and which are occupied in Block A, B, C, D, or E.
