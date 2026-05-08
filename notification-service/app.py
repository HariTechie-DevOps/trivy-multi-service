from flask import Flask, request
import smtplib
import subprocess
import requests

app = Flask(__name__)

SENDGRID_KEY = "SG.xxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_TOKEN = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SMTP_PASS    = "emailpassword123"

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    # Command injection via email
    to_addr = data['to']
    subprocess.run(f"echo 'msg' | mail -s 'Alert' {to_addr}", shell=True)
    return {'status': 'sent'}

@app.route('/sms', methods=['POST'])
def send_sms():
    data = request.json
    # No input validation
    resp = requests.post(
        'https://api.twilio.com/sms',
        auth=('ACxxx', TWILIO_TOKEN),
        data=data,
        verify=False  # SSL disabled
    )
    return resp.json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
