-- ====================================================================
-- DBMS PROJECT: HOSTEL ROOM BOOKING SYSTEM
-- Schema: 5 Blocks with 20 Rooms Each (100 Rooms Total)
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. BLOCKS TABLE (5 Blocks)
CREATE TABLE IF NOT EXISTS blocks (
    block_id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_name TEXT NOT NULL UNIQUE
);

-- 2. ROOMS TABLE (20 Rooms per block)
CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    block_id INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    FOREIGN KEY (block_id) REFERENCES blocks(block_id) ON DELETE CASCADE,
    UNIQUE(block_id, room_number)
);

-- 3. STUDENTS TABLE (For CRUD Operations)
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    gender TEXT,
    department TEXT,
    phone TEXT,
    room_id INTEGER UNIQUE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id) ON DELETE SET NULL
);

-- 4. INSERT 5 BLOCKS
INSERT OR IGNORE INTO blocks (block_id, block_name) VALUES
(1, 'Block A'),
(2, 'Block B'),
(3, 'Block C'),
(4, 'Block D'),
(5, 'Block E');

-- 5. INSERT 20 ROOMS PER BLOCK (100 Rooms total)
INSERT OR IGNORE INTO rooms (block_id, room_number) VALUES
-- Block A (101-120)
(1, 'A-101'), (1, 'A-102'), (1, 'A-103'), (1, 'A-104'), (1, 'A-105'),
(1, 'A-106'), (1, 'A-107'), (1, 'A-108'), (1, 'A-109'), (1, 'A-110'),
(1, 'A-111'), (1, 'A-112'), (1, 'A-113'), (1, 'A-114'), (1, 'A-115'),
(1, 'A-116'), (1, 'A-117'), (1, 'A-118'), (1, 'A-119'), (1, 'A-120'),

-- Block B (201-220)
(2, 'B-201'), (2, 'B-202'), (2, 'B-203'), (2, 'B-204'), (2, 'B-205'),
(2, 'B-206'), (2, 'B-207'), (2, 'B-208'), (2, 'B-209'), (2, 'B-210'),
(2, 'B-211'), (2, 'B-212'), (2, 'B-213'), (2, 'B-214'), (2, 'B-215'),
(2, 'B-216'), (2, 'B-217'), (2, 'B-218'), (2, 'B-219'), (2, 'B-220'),

-- Block C (301-320)
(3, 'C-301'), (3, 'C-302'), (3, 'C-303'), (3, 'C-304'), (3, 'C-305'),
(3, 'C-306'), (3, 'C-307'), (3, 'C-308'), (3, 'C-309'), (3, 'C-310'),
(3, 'C-311'), (3, 'C-312'), (3, 'C-313'), (3, 'C-314'), (3, 'C-315'),
(3, 'C-316'), (3, 'C-317'), (3, 'C-318'), (3, 'C-319'), (3, 'C-320'),

-- Block D (401-420)
(4, 'D-401'), (4, 'D-402'), (4, 'D-403'), (4, 'D-404'), (4, 'D-405'),
(4, 'D-406'), (4, 'D-407'), (4, 'D-408'), (4, 'D-409'), (4, 'D-410'),
(4, 'D-411'), (4, 'D-412'), (4, 'D-413'), (4, 'D-414'), (4, 'D-415'),
(4, 'D-416'), (4, 'D-417'), (4, 'D-418'), (4, 'D-419'), (4, 'D-420'),

-- Block E (501-520)
(5, 'E-501'), (5, 'E-502'), (5, 'E-503'), (5, 'E-504'), (5, 'E-505'),
(5, 'E-506'), (5, 'E-507'), (5, 'E-508'), (5, 'E-509'), (5, 'E-510'),
(5, 'E-511'), (5, 'E-512'), (5, 'E-513'), (5, 'E-514'), (5, 'E-515'),
(5, 'E-516'), (5, 'E-517'), (5, 'E-518'), (5, 'E-519'), (5, 'E-520');
