from flask import Flask, request, jsonify
import smtplib
import random
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_cors import CORS  # Import Flask-CORS to enable cross-origin requests

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store OTP and expiration time
otp_data = {}

# Gmail credentials (Replace with your Gmail email and App Password)
GMAIL_USER = "ajaynegiaaaaaaa@gmail.com"  # Replace with your Gmail address
GMAIL_PASSWORD = ""  # Replace with your 16-character App Password

# Function to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to send OTP via Gmail
def send_otp_email(to_email, otp):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = 'Your OTP Code'

        # Body of the email
        body = f'Your OTP is: {otp}'
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(GMAIL_USER, GMAIL_PASSWORD)  # Login using your Gmail credentials and App Password
            server.sendmail(GMAIL_USER, to_email, msg.as_string())

        print("OTP sent successfully!")
    except Exception as e:
        print(f"Error sending OTP email: {e}")

# Endpoint to request an OTP
@app.route('/generate_otp', methods=['POST'])
def generate_otp_route():
    email = request.json.get("email")  # Get the email address from the client
    if not email:
        return jsonify({"status": "fail", "message": "Email not provided!"}), 400

    otp = generate_otp()
    otp_data['otp'] = otp
    otp_data['expires_at'] = time.time() + 300  # OTP expires in 5 minutes

    # Send OTP to the provided email
    send_otp_email(email, otp)

    return jsonify({"status": "success", "message": "OTP sent to your email!"})

# Endpoint to verify the OTP
@app.route('/verify_otp', methods=['POST'])
def verify_otp_route():
    user_otp = request.json.get("otp")
    if not user_otp:
        return jsonify({"status": "fail", "message": "OTP not provided!"}), 400
    
    current_time = time.time()
    if otp_data.get('otp') == int(user_otp) and current_time < otp_data.get('expires_at'):
        return jsonify({"status": "success", "message": "OTP is valid!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid or expired OTP!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
