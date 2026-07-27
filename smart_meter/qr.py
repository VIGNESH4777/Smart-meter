import qrcode


def generate_qr_code(meter_info, output_path):
    qr = qrcode.make(meter_info)
    qr.save(output_path)
    return output_path
