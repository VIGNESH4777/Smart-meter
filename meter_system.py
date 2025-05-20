import sqlite3
import qrcode
import smtplib
from email.message import EmailMessage
import os

def init_db():
    conn = sqlite3.connect("meter_readings.db")
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
    conn = sqlite3.connect("meter_readings.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO meter_data VALUES
        ('MTR123', 'Sub-A1', 'John Doe', 2546, '2025-06-10', 'dsv3352@gmail.com'),
        ('MTR456', 'Sub-B2', 'Jane Smith', 1879, '2025-06-08', 'jane@example.com')
    """)
    conn.commit()
    conn.close()

def generate_qr_code(meter_number):
    conn = sqlite3.connect("meter_readings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meter_data WHERE meter_number = ?", (meter_number,))
    data = cursor.fetchone()
    conn.close()

    if not data:
        print("Meter not found.")
        return

    meter_info = {
        "meter_number": data[0],
        "sub_division": data[1],
        "customer_name": data[2],
        "units_consumed": data[3],
        "last_due_date": data[4],
        "email": data[5]
    }

    qr = qrcode.make(meter_info)
    qr_path = f"qr_{meter_number}.png"
    qr.save(qr_path)
    print(f"QR Code for {meter_number} saved as {qr_path}")

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "youremail@example.com"  # CHANGE THIS to your email
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("dsv3352@gmail.com", "qrcg dboz yscb hlhz")  # CHANGE THIS to your app password
            server.send_message(msg)
            print(f"Email sent to {to_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def simulate_scan_and_notify(meter_number):
    conn = sqlite3.connect("meter_readings.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM meter_data WHERE meter_number = ?", (meter_number,))
    data = cursor.fetchone()
    conn.close()

    if not data:
        print("Meter not found.")
        return

    message = f"""
Meter Number: {data[0]}
Customer: {data[2]}
Sub-Division: {data[1]}
Units Consumed: {data[3]}
Due Date: {data[4]}
"""
    print("\nScanned Message:", message)
    send_email(data[5], "Electricity Bill Details", message)

if __name__ == '__main__':
    if not os.path.exists("meter_readings.db"):
        init_db()
        insert_sample_data()

    generate_qr_code('MTR123')
    simulate_scan_and_notify('MTR123')
