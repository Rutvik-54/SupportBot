from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from google import genai
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
print(os.getenv("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"))

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('serve_index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('serve_index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('serve_index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/signup.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('auth/signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('auth/signup.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration', 'danger')
            return render_template('auth/signup.html')
    
    return render_template('auth/signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Configure Gemini (demo: hardcoded key; in production, use .env)
client = genai.Client(api_key="AIzaSyDCx5jegRfoqODU_14xvW5iRn0kjlp3x7Q")

# Emotional support responses
EMOTIONAL_SUPPORT_PROMPTS = {
    'sad': [
        "I'm sorry to hear you're feeling down. Would you like to talk more about what's bothering you?",
        "It's okay to feel sad sometimes. Remember that this feeling won't last forever.",
        "I'm here to listen and support you. Would you like to share more about what's making you feel this way?"
    ],
    'anxious': [
        "I understand that anxiety can be overwhelming. Let's take a deep breath together.",
        "It's normal to feel anxious sometimes. Would you like to talk about what's causing your anxiety?",
        "Remember that you're not alone in this. I'm here to support you through this difficult time."
    ],
    'angry': [
        "I can see that you're feeling angry. Would you like to talk about what happened?",
        "It's okay to feel angry, but let's try to understand what's causing these feelings.",
        "I'm here to listen without judgment. Would you like to share what's making you feel this way?"
    ],
    'happy': [
        "I'm glad to hear you're feeling happy! What's bringing you joy today?",
        "That's wonderful! It's great to hear about positive moments in your life.",
        "Your happiness is contagious! Would you like to share more about what's making you feel good?"
    ]
}

def analyze_emotion(text):
    """Analyze the emotional content of the text using Gemini API (genai.Client)."""
    try:
        prompt = "You are an emotional analysis AI. Analyze the following text and respond with a single emotion: 'sad', 'anxious', 'angry', 'happy', or 'neutral'. Text: " + text
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        emotion = response.text.strip().lower()
        return emotion
    except Exception as e:
        print(f"Error in emotion analysis (Gemini): {e}")
        return "neutral"

def get_supportive_response(emotion, user_message):
    """Generate a supportive response based on the detected emotion using Gemini API (genai.Client)."""
    try:
        prompt = "You are a supportive and empathetic AI companion. Provide emotional support and understanding in your responses. Keep responses concise and focused on emotional support. The user is feeling " + emotion + " and says: " + user_message
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generating response (Gemini): {e}")
        # Fallback: always return a neutral fallback message (for demo purposes)
        neutral_prompt = ["Hello! How are you feeling today? I'm here to listen and support you."]
        import random
        return random.choice(neutral_prompt)

@app.route('/')
@login_required
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        if not user_message:
             return jsonify({'error': 'No message provided'}), 400
        emotion = analyze_emotion(user_message)
        print(f"User message: {user_message}")
        print(f"Detected emotion (Gemini): {emotion}")
        response = get_supportive_response(emotion, user_message)
        print(f"Bot response (Gemini): {response}")
        return jsonify({'response': response})
    except Exception as e:
         print(f"Error in chat endpoint: {e}")
         return jsonify({'error': 'An error occurred while processing your message'}), 500

if __name__ == '__main__':
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY not found in environment variables")
    
    app.run(debug=True, port=5000) 