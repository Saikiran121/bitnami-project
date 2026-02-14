from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Security: In a real app, these would be sensitive keys
# We will use environment variables which will be populated from Sealed Secrets
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "guest")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_insecure_password")
DB_PORT = os.getenv("DB_PORT", "5432")
API_KEY = os.getenv("API_KEY", "default_insecure_key")

@app.route('/')
def index():
    budget_data = [
        {"item": "Server Costs", "amount": 1200},
        {"item": "Software Licenses", "amount": 450},
        {"item": "Network Bandwidth", "amount": 300},
    ]
    total = sum(d['amount'] for d in budget_data)
    
    # Check if we are running in a "secure" environment (i.e. if secrets were provided)
    is_secure = (DB_PASSWORD != "default_insecure_password")
    
    db_config = {
        "host": DB_HOST,
        "user": DB_USER,
        "port": DB_PORT
    }
    
    return render_template('index.html', budget_data=budget_data, total=total, is_secure=is_secure, db_config=db_config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
