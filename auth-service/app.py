from flask import Flask, request
import jwt
import bcrypt
import hashlib

app = Flask(__name__)

# Hardcoded secrets
SECRET_KEY   = "super-secret-jwt-key-12345"
API_KEY      = "AKIAIOSFODNN7EXAMPLE"
DB_PASSWORD  = "admin123"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    # Weak MD5 hash for password
    pw_hash = hashlib.md5(data['password'].encode()).hexdigest()
    token = jwt.encode({'user': data['user']}, SECRET_KEY, algorithm='HS256')
    return {'token': token}

@app.route('/verify', methods=['POST'])
def verify():
    token = request.json.get('token')
    # No expiry check - vulnerable
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return payload

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

