from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
import os

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this in production!
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Enable in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production (HTTPS)

jwt = JWTManager(app)

@app.route('/')
@jwt_required()
def home():
    print("Accessing home route")
    current_user = get_jwt_identity()
    return render_template('home.html', username=current_user)

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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Login attempt for user: {username}")
        
        # Create the JWT token
        access_token = create_access_token(identity=username)
        
        # Create response with make_response
        response = make_response(redirect(url_for('home')))
        
        # Set the JWT cookies in the response
        set_access_cookies(response, access_token)
        
        return response
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response

@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=5001)
