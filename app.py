from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# Set a secret key for session management
app.secret_key = 'your-secret-key-here'  # In production, use a secure random key

@app.route('/')
def home():
    print("Accessing home route")
    if 'username' not in session:
        return redirect(url_for('login'))
    return f'Hello, {session["username"]}! <a href="{url_for("logout")}">Logout</a>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Accessing register route")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Registration attempt for user: {username}")
        # Here you would typically save the user to a database
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Accessing login route")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt for user: {username}")
        # Here you would typically validate the credentials
        session['username'] = username  # Store username in session
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Current working directory: {os.getcwd()}")
    print("Available routes:")
    print("  - http://127.0.0.1:5001/")
    print("  - http://127.0.0.1:5001/register")
    print("  - http://127.0.0.1:5001/login")
    print("  - http://127.0.0.1:5001/logout")
    app.run(debug=True, port=5001)
