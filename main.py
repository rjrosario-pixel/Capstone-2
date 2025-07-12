from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from models.db_models import db, PhishingURL, BlacklistURL, User
from features import extract_features
import joblib

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow credentials for session cookies

# Config
app.config['SECRET_KEY'] = 'super-secret-key'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:06032004@localhost:5432/phishing_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Load ML model
model = joblib.load("phishing_model.pkl")

# ------------------------
# ROUTES
# ------------------------

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not password or not username:
        return jsonify({'message': 'Missing fields'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 409

    try:
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        print("Registration error:", e)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'result': 'Unknown'})

    try:
        # Check blacklist
        if BlacklistURL.query.filter_by(url=url).first():
            print(f"⚠️ URL found in blacklist: {url}")
            return jsonify({'result': 'Phish'})
        else:
            print(f"✅ URL NOT in blacklist. Using ML for: {url}")

        # Predict
        features = extract_features(url)
        print("Features:", features)
        prediction = model.predict([features])[0]
        print("Prediction:", prediction)

        result = 'Phish' if prediction == 1 else 'Safe'
        return jsonify({'result': result})

    except Exception as e:
        print("Error:", e)
        return jsonify({'result': 'Unknown'}), 500

if __name__ == '__main__':
    app.run(debug=True)
