from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import cv2
from pyzbar.pyzbar import decode
import hmac
import base64
import hashlib
import time
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)
camera = None  # Camera is initially off
secret_key = "supersecretkey"
uri = "mongodb+srv://samriddh_kumar:sam123@tracknclassify.kjmrfft.mongodb.net/?retryWrites=true&w=majority&appName=TrackNClassify"

def verify_token(token, secret_key, tolerance=1):
    current_time = int(time.time() / 60)
    for i in range(-tolerance, tolerance + 1):
        timestamp = current_time + i
        msg = str(timestamp).encode()
        hmac_obj = hmac.new(secret_key.encode(), msg, hashlib.sha256)
        expected_token = base64.urlsafe_b64encode(hmac_obj.digest()).decode().strip('=')
        if hmac.compare_digest(expected_token, token):
            return True
    return False

def verify_employee_data(qr_data):
    try:
        *data_parts, token = qr_data.split(',')
        employee_id, employee_name, employee_age = data_parts
        employee_age = int(employee_age)

        if not verify_token(token, secret_key):
            return "Invalid or expired QR code"
        
        with MongoClient(uri) as client:
            db = client['Employee']
            collection = db['Employee']
            
            found_document = collection.find_one({
                "ID": employee_id,
                "Name": employee_name,
                "Age": employee_age
            })

            if found_document:
                return f"{found_document['Name']} is an Employee"
            else:
                return "Not an Employee"
    except Exception as e:
        return f"An error occurred: {e}"

def generate_frames():
    global camera  # Use the global camera variable
    while True:
        if camera is not None:  # Only capture frames if the camera is turned on
            success, frame = camera.read()
            if not success:
                break
            else:
                for barcode in decode(frame):
                    qr_data = barcode.data.decode('utf-8')
                    result = verify_employee_data(qr_data)
                    socketio.emit('scan_result', result)
                    
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera')
def start_camera():
    global camera  # Use the global camera variable
    if camera is None:
        camera = cv2.VideoCapture(0)  # Start the camera
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_camera')
def stop_camera():
    global camera  # Use the global camera variable
    if camera is not None:  # If the camera is running
        camera.release()  # Release the camera resources
        camera = None  # Set the camera to None to indicate it's off
    return 'Camera stopped'

if __name__ == '__main__':
    
    socketio.run(app, debug=True)
 