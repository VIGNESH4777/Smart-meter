# Smart Meter Project

This project stores smart meter readings, generates a QR code for a meter, and emails bill details.

## Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set your email credentials.

## Run

```bash
python meter_system.py --meter MTR123 --generate-qr --send-email
```

## Project structure

- `meter_system.py`: project entrypoint
- `smart_meter/`: package modules
- `smart_meter/db.py`: database helpers
- `smart_meter/qr.py`: QR code generation
- `smart_meter/emailer.py`: email sending
- `smart_meter/main.py`: CLI and orchestration
- `.env.example`: example configuration
