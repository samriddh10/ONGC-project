from flask import Flask, render_template, send_file
import qrcode
import time
import hmac
import base64
import hashlib
import io

app = Flask(__name__)

# Function to generate a time-based token
def generate_token(secret_key):
    timestamp = int(time.time() / 60)  # Time step of 60 seconds
    msg = str(timestamp).encode()
    hmac_obj = hmac.new(secret_key.encode(), msg, hashlib.sha256)
    token = base64.urlsafe_b64encode(hmac_obj.digest()).decode().strip('=')
    return token

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr')
def generate_qr():
    # Data and secret key
    employee_data = {
        "ID": "2",
        "Name": "Samriddh",
        "Age": 19
    }
    secret_key = "supersecretkey"
    data = f'{employee_data["ID"]},{employee_data["Name"]},{employee_data["Age"]}'
    token = generate_token(secret_key)

    # Combine data with the token
    dynamic_data = f'{data},{token}'

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add dynamic data to the QR code
    qr.add_data(dynamic_data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image in a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
