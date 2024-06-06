import cv2
from pyzbar.pyzbar import decode
import hmac
import base64
import hashlib
import time
import pymongo
from pymongo import MongoClient

# Function to scan QR code
def scan_qr_code():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height

    start_time = time.time()
    
    while True:
        success, frame = cam.read()
        if not success:
            break
        
        for barcode in decode(frame):
            qr_data = barcode.data.decode('utf-8')
            cam.release()
            cv2.destroyAllWindows()
            return qr_data
        
        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or (time.time() - start_time) > 10:
            break
    
    cam.release()
    cv2.destroyAllWindows()
    return None

# Function to verify time-based token
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

# Function to verify employee data
def verify_employee_data(qr_data):
    # Split the data and token
    *data_parts, token = qr_data.split(',')
    employee_id, employee_name, employee_age = data_parts
    employee_age = int(employee_age)
    
    # Secret key used to generate the token
    secret_key = "supersecretkey"
    
    # Verify the token
    if not verify_token(token, secret_key):
        print("Invalid or expired QR code")
        return
    
    # MongoDB connection URI
    uri = "mongodb+srv://samriddh_kumar:sam123@tracknclassify.kjmrfft.mongodb.net/?retryWrites=true&w=majority&appName=TrackNClassify"
    
    try:
        client = MongoClient(uri)
        db = client['Employee']
        collection = db['Employee']
        
        # Find the document in the collection
        found_document = collection.find_one({
            "ID": employee_id,
            "Name": employee_name,
            "Age": employee_age
        })
        
        if found_document:
            print(f"{found_document['Name']} is an Employee")
        else:
            print("Not an Employee")
    except pymongo.errors.ConnectionError as e:
        print(f"Database connection error: {e}")
    finally:
        client.close()

# Main function to run the scanner and verify data
def main():
    print("Scanning QR code. Please show the QR code to the camera.")
    qr_data = scan_qr_code()
    
    if qr_data:
        print(f"QR Code data: {qr_data}")
        verify_employee_data(qr_data)
    else:
        print("No QR code found or scan timed out. The person is a visitor.")

# Run the main function
if __name__ == "__main__":
    main()
