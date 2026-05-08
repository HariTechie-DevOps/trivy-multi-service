from flask import Flask, request
import sqlite3
import pickle
import yaml

app = Flask(__name__)

GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
AWS_SECRET   = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route('/users')
def get_users():
    user_id = request.args.get('id')
    conn = sqlite3.connect(':memory:')
    # SQL Injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return {'query': query}

@app.route('/import', methods=['POST'])
def import_user():
    data = request.data
    # Insecure deserialization
    obj = pickle.loads(data)  # BAD: RCE possible
    return str(obj)

@app.route('/config')
def get_config():
    # YAML injection
    config = yaml.load(request.data, Loader=yaml.Loader)  # BAD
    return str(config)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
