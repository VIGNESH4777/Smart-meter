import os
import sqlite3

DB_PATH = "meter_readings.db"

SAMPLE_DATA = [
    ('MTR123', 'Sub-A1', 'John Doe', 2546, '2025-06-10', 'dsv3352@gmail.com'),
    ('MTR456', 'Sub-B2', 'Jane Smith', 1879, '2025-06-08', 'jane@example.com')
]


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meter_data (
            meter_number TEXT PRIMARY KEY,
            sub_division TEXT,
            customer_name TEXT,
            units_consumed INTEGER,
            last_due_date TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR REPLACE INTO meter_data VALUES (?, ?, ?, ?, ?, ?)",
        SAMPLE_DATA
    )
    conn.commit()
    conn.close()


def get_meter_data(meter_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meter_data WHERE meter_number = ?", (meter_number,))
    data = cursor.fetchone()
    conn.close()
    return data


def ensure_db():
    if not os.path.exists(DB_PATH):
        init_db()
        insert_sample_data()
