from flask import Flask, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Hardcoded payment credentials
STRIPE_KEY   = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"
PAYPAL_SECRET = "EBWKjlELKMYqRNQ6sYvFo64FtaaN"
DB_CONN      = "postgresql://admin:admin123@db:5432/payments"

@app.route('/charge', methods=['POST'])
def charge():
    data = request.json
    # Unsafe external request — no SSL verify
    resp = requests.post(
        'https://api.payment.com/charge',
        json=data,
        verify=False  # BAD: SSL disabled
    )
    return resp.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    # XXE vulnerability — unsafe XML parsing
    xml_data = request.data
    tree = ET.fromstring(xml_data)  # BAD: no defusedxml
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
