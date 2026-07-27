import argparse
from .db import ensure_db, get_meter_data
from .qr import generate_qr_code
from .emailer import send_email


def build_meter_info(data):
    return {
        'meter_number': data[0],
        'sub_division': data[1],
        'customer_name': data[2],
        'units_consumed': data[3],
        'last_due_date': data[4],
        'email': data[5],
    }


def format_bill_message(data):
    return (
        f"Meter Number: {data[0]}\n"
        f"Customer: {data[2]}\n"
        f"Sub-Division: {data[1]}\n"
        f"Units Consumed: {data[3]}\n"
        f"Due Date: {data[4]}\n"
    )


def main():
    parser = argparse.ArgumentParser(description='Smart meter tool')
    parser.add_argument('--meter', required=True, help='Meter number to process')
    parser.add_argument('--generate-qr', action='store_true', help='Generate QR code for the meter')
    parser.add_argument('--send-email', action='store_true', help='Send bill email for the meter')
    args = parser.parse_args()

    ensure_db()

    data = get_meter_data(args.meter)
    if not data:
        print(f"Meter {args.meter} not found.")
        return

    meter_info = build_meter_info(data)

    if args.generate_qr:
        qr_path = f"qr_{args.meter}.png"
        generate_qr_code(meter_info, qr_path)
        print(f"QR Code saved as {qr_path}")

    if args.send_email:
        message = format_bill_message(data)
        send_email(data[5], 'Electricity Bill Details', message)
        print(f"Email sent to {data[5]}")

    if not args.generate_qr and not args.send_email:
        print('No action specified. Use --generate-qr or --send-email.')
