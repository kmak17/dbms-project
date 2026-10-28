-- ====================================================================
-- DBMS PROJECT: HOSTEL ROOM BOOKING SYSTEM
-- Core SQL Queries (CRUD Operations & Room Status)
-- ====================================================================

-- 1. CREATE: Insert a new student and allocate a room
INSERT INTO students (roll_no, name, gender, department, phone, room_id)
VALUES ('26D2DIT001', 'Aarav Mehta', 'Male', 'Information Technology', '9876543210', 1);

-- 2. READ: View all students with their block and room
SELECT 
    s.student_id,
    s.roll_no,
    s.name,
    s.gender,
    s.department,
    s.phone,
    b.block_name,
    r.room_number
FROM students s
LEFT JOIN rooms r ON s.room_id = r.room_id
LEFT JOIN blocks b ON r.block_id = b.block_id
ORDER BY s.student_id DESC;

-- 3. READ: View all available (unoccupied) rooms across the 5 blocks
SELECT 
    r.room_id,
    b.block_name,
    r.room_number
FROM rooms r
JOIN blocks b ON r.block_id = b.block_id
WHERE r.room_id NOT IN (
    SELECT room_id FROM students WHERE room_id IS NOT NULL
)
ORDER BY b.block_id, r.room_number;

-- 4. UPDATE: Update student contact or reassign room
UPDATE students
SET name = 'Aarav M. Mehta',
    phone = '9876599999',
    room_id = 2
WHERE student_id = 1;

-- 5. DELETE: Delete a student record (room is automatically freed up)
DELETE FROM students
WHERE student_id = 1;
