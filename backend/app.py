"""
Kolan Hanmanth Reddy - Political Leader Website
Flask Backend Application
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
import os
import json
from functools import wraps
import hashlib

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Initialize Flask app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..'), static_url_path='')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'kolan-hanmanth-reddy-2024-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://kishore:kishore*123@72.61.254.168:5432/khr_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Email Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@kolanhanmanthreddy.com')

# Debug email configuration (remove in production)
print("=" * 50)
print("EMAIL CONFIGURATION:")
print(f"MAIL_SERVER: {app.config['MAIL_SERVER']}")
print(f"MAIL_PORT: {app.config['MAIL_PORT']}")
print(f"MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
print(f"MAIL_USE_SSL: {app.config['MAIL_USE_SSL']}")
print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
print(f"MAIL_PASSWORD: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
print(f"MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
print("=" * 50)

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)

# Initialize Groq AI Client (graceful fallback if key is missing)
try:
    groq_api_key = os.getenv('GROQ_API_KEY')
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
    else:
        print("WARNING: GROQ_API_KEY not set. AI chat will be unavailable.")
        groq_client = None
except Exception as e:
    print(f"WARNING: Failed to initialize Groq client: {e}")
    groq_client = None

# ============================================
# DATABASE MODELS
# ============================================

class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, resolved, rejected
    reference_number = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_notes = db.Column(db.Text, default='')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'area': self.area,
            'category': self.category,
            'subject': self.subject,
            'message': self.message,
            'address': self.address,
            'status': self.status,
            'reference_number': self.reference_number,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    category = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='received')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'category': self.category,
            'rating': self.rating,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class SkillsRegistration(db.Model):
    __tablename__ = 'skills_registrations'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    education = db.Column(db.String(50), nullable=False)
    institution = db.Column(db.String(150))
    location = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    confirmation_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'dob': self.dob.strftime('%Y-%m-%d'),
            'education': self.education,
            'institution': self.institution,
            'location': self.location,
            'city': self.city,
            'motivation': self.motivation,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='received')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='moderator')  # admin, moderator
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()


class CommunityImpact(db.Model):
    __tablename__ = 'community_impacts'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge = db.Column(db.String(100), nullable=False)  # e.g., Healthcare, Youth, Outreach
    image_url = db.Column(db.String(500), nullable=False)
    overlay_title = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'badge': self.badge,
            'image_url': self.image_url,
            'overlay_title': self.overlay_title,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # e.g., Politics, Community, Healthcare
    news_date = db.Column(db.String(100), nullable=False)  # e.g., "December 2023"
    image_url = db.Column(db.String(500), nullable=True)  # Optional
    link_url = db.Column(db.String(500), nullable=True)  # Optional external link
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'news_date': self.news_date,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class MediaRecognition(db.Model):
    __tablename__ = 'media_recognition'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)  # e.g., "The Hans India", "Official Social Media"
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)  # Font Awesome icon class e.g., "fas fa-newspaper"
    link_url = db.Column(db.String(500), nullable=False)
    link_text = db.Column(db.String(100), default='Read Article')  # Button text
    media_type = db.Column(db.String(50), nullable=False)  # e.g., "Press", "Social Media", "TV", "Radio"
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'link_url': self.link_url,
            'link_text': self.link_text,
            'media_type': self.media_type,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    designation = db.Column(db.String(200), nullable=False)  # e.g., "Community Resident", "Youth Volunteer"
    location = db.Column(db.String(200), nullable=False)  # e.g., "Girinagar Area", "Quthbullapur NGO"
    testimonial_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)  # Star rating 1-5
    avatar_icon = db.Column(db.String(50), default='fas fa-user')  # Font Awesome icon
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation,
            'location': self.location,
            'testimonial_text': self.testimonial_text,
            'rating': self.rating,
            'avatar_icon': self.avatar_icon,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


# Gallery Model for Photos and Videos
class Gallery(db.Model):
    __tablename__ = 'gallery'
    
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    media_url = db.Column(db.String(500), nullable=False)  # Path to photo or video file
    media_type = db.Column(db.String(20), nullable=False)  # 'photo' or 'video'
    thumbnail_url = db.Column(db.String(500))  # Thumbnail for videos (optional)
    video_embed_url = db.Column(db.String(500))  # YouTube/Vimeo embed URL (optional)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'thumbnail_url': self.thumbnail_url,
            'video_embed_url': self.video_embed_url,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


# ============================================
# FILE UPLOAD HELPERS
# ============================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_filename_custom(filename):
    """Create a secure filename"""
    # Get file extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    # Create unique filename with timestamp
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    secure_name = f"community_impact_{timestamp}.{ext}"
    return secure_name


# ============================================
# FILE UPLOAD ENDPOINTS
# ============================================

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Upload an image file"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'File type not allowed. Use: png, jpg, jpeg, gif, webp'}), 400
        
        # Create secure filename
        filename = secure_filename_custom(file.filename)
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Return relative URL
        image_url = f"images/{filename}"
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'image_url': image_url,
            'filename': filename
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# API ROUTES - FORM SUBMISSIONS
# ============================================

@app.route('/api/complaint', methods=['POST'])
def submit_complaint():
    """Submit a complaint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'area', 'category', 'subject', 'message', 'address']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create complaint ID
        complaint_id = f"COMP_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        ref_number = f"REF-{datetime.utcnow().year}-{Complaint.query.count() + 1:05d}"
        
        # Create complaint object
        complaint = Complaint(
            id=complaint_id,
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            area=data['area'],
            category=data['category'],
            subject=data['subject'],
            message=data['message'],
            address=data['address'],
            reference_number=ref_number
        )
        
        db.session.add(complaint)
        db.session.commit()
        
        # Send confirmation email
        send_complaint_confirmation_email(complaint)
        
        return jsonify({
            'success': True,
            'message': 'Complaint submitted successfully',
            'reference_number': ref_number
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'category', 'rating', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Validate rating
        rating = int(data['rating'])
        if rating < 1 or rating > 5:
            return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
        
        # Create feedback ID
        feedback_id = f"FB_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Create feedback object
        feedback = Feedback(
            id=feedback_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            category=data['category'],
            rating=rating,
            message=data['message']
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        # Send confirmation email
        send_feedback_confirmation_email(feedback)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback!'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/skills-registration', methods=['POST'])
def register_skills():
    """Register for skills program"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'email', 'dob', 'education', 'location', 'city', 'motivation']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create registration ID
        registration_id = f"SKL_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Create registration object
        registration = SkillsRegistration(
            id=registration_id,
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            dob=datetime.strptime(data['dob'], '%Y-%m-%d').date(),
            education=data['education'],
            institution=data.get('institution', ''),
            location=data['location'],
            city=data['city'],
            motivation=data['motivation']
        )
        
        db.session.add(registration)
        db.session.commit()
        
        # Send confirmation email
        send_skills_confirmation_email(registration)
        registration.confirmation_sent = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful! Confirmation email sent.'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create contact ID
        contact_id = f"CNT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Create contact object
        contact = Contact(
            id=contact_id,
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            subject=data['subject'],
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()
        
        # Send confirmation email
        send_contact_confirmation_email(contact)
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully!'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# EMAIL FUNCTIONS
# ============================================

def send_complaint_confirmation_email(complaint):
    """Send complaint confirmation email"""
    try:
        msg = Message(
            subject=f'Complaint Received - Reference: {complaint.reference_number}',
            recipients=[complaint.email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #ff9500;">Complaint Acknowledgment</h2>
                    <p>Dear {complaint.name},</p>
                    <p>We have received your complaint and it has been registered in our system.</p>
                    <p><strong>Reference Number: {complaint.reference_number}</strong></p>
                    <p><strong>Category: {complaint.category}</strong></p>
                    <p><strong>Subject: {complaint.subject}</strong></p>
                    <p>Your complaint will be reviewed and addressed within 7 working days.</p>
                    <p>You can track the status using your reference number.</p>
                    <p>Thank you for bringing this to our attention.</p>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        Kolan Hanmanth Reddy<br>
                        Senior Congress Leader, Quthbullapur
                    </p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        print(f"✓ Complaint confirmation email sent to {complaint.email} (Ref: {complaint.reference_number})")
        return True
    except Exception as e:
        import traceback
        print(f"✗ Error sending complaint email to {complaint.email}: {str(e)}")
        print(traceback.format_exc())
        return False


def send_feedback_confirmation_email(feedback):
    """Send feedback confirmation email"""
    try:
        msg = Message(
            subject='We Value Your Feedback',
            recipients=[feedback.email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #ff9500;">Thank You for Your Feedback</h2>
                    <p>Dear {feedback.name},</p>
                    <p>We have received your feedback and appreciate your input.</p>
                    <p><strong>Category: {feedback.category}</strong></p>
                    <p><strong>Rating: {feedback.rating}/5</strong></p>
                    <p>Your feedback helps us improve our services and better serve the community.</p>
                    <p>Thank you for your valuable suggestions.</p>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        Kolan Hanmanth Reddy<br>
                        Senior Congress Leader, Quthbullapur
                    </p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        print(f"✓ Feedback confirmation email sent to {feedback.email}")
        return True
    except Exception as e:
        import traceback
        print(f"✗ Error sending feedback email to {feedback.email}: {str(e)}")
        print(traceback.format_exc())
        return False


def send_skills_confirmation_email(registration):
    """Send skills registration confirmation email"""
    try:
        msg = Message(
            subject='Registration Confirmed - Skills Development Program',
            recipients=[registration.email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #ff9500;">Skills Development Program Registration</h2>
                    <p>Dear {registration.name},</p>
                    <p>Your registration for the Skills Development Program has been received.</p>
                    <p><strong>Education Level: {registration.education}</strong></p>
                    <p><strong>Location: {registration.location}</strong></p>
                    <p>Your application is currently under review. You will receive further updates shortly.</p>
                    <p>Status updates will be sent to this email address.</p>
                    <p>If you have any questions, please don't hesitate to contact us.</p>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        Kolan Hanmanth Reddy<br>
                        Senior Congress Leader, Quthbullapur
                    </p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        print(f"✓ Skills confirmation email sent to {registration.email}")
        return True
    except Exception as e:
        import traceback
        print(f"✗ Error sending skills confirmation email to {registration.email}: {str(e)}")
        print(traceback.format_exc())
        return False


def send_contact_confirmation_email(contact):
    """Send contact confirmation email"""
    try:
        msg = Message(
            subject='Message Received',
            recipients=[contact.email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #ff9500;">Message Acknowledgment</h2>
                    <p>Dear {contact.name},</p>
                    <p>We have received your message and will get back to you soon.</p>
                    <p><strong>Subject: {contact.subject}</strong></p>
                    <p>Thank you for reaching out to us.</p>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        Kolan Hanmanth Reddy<br>
                        Senior Congress Leader, Quthbullapur
                    </p>
                </body>
            </html>
            """
        )
        mail.send(msg)
        print(f"✓ Contact confirmation email sent to {contact.email}")
        return True
    except Exception as e:
        import traceback
        print(f"✗ Error sending contact email to {contact.email}: {str(e)}")
        print(traceback.format_exc())
        return False


# ============================================
# GENERAL ROUTES
# ============================================

@app.route('/')
def index():
    """Home page"""
    return send_from_directory(os.path.dirname(app.static_folder), 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    if filename.endswith('.html'):
        return send_from_directory(os.path.dirname(app.static_folder), filename)
    else:
        return send_from_directory(os.path.dirname(app.static_folder), filename)


# ============================================
# DATA RETRIEVAL ENDPOINTS (for admin dashboard)
# ============================================

@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    """Get all complaints"""
    try:
        complaints = Complaint.query.all()
        data = [{
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'phone': c.phone,
            'area': c.area,
            'category': c.category,
            'subject': c.subject,
            'message': c.message,
            'address': c.address,
            'status': c.status,
            'reference_number': c.reference_number,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in complaints]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/feedback-list', methods=['GET'])
def get_feedback_list():
    """Get all feedback"""
    try:
        feedbacks = Feedback.query.all()
        data = [{
            'id': f.id,
            'name': f.name,
            'email': f.email,
            'phone': f.phone,
            'category': f.category,
            'rating': f.rating,
            'message': f.message,
            'status': f.status,
            'created_at': f.created_at.isoformat() if f.created_at else None
        } for f in feedbacks]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/skills-list', methods=['GET'])
def get_skills_list():
    """Get all skills registrations"""
    try:
        registrations = SkillsRegistration.query.all()
        data = [{
            'id': r.id,
            'name': r.name,
            'email': r.email,
            'phone': r.phone,
            'dob': r.dob,
            'education': r.education,
            'institution': r.institution,
            'location': r.location,
            'city': r.city,
            'motivation': r.motivation,
            'status': r.status,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in registrations]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/contacts-list', methods=['GET'])
def get_contacts_list():
    """Get all contact messages"""
    try:
        contacts = Contact.query.all()
        data = [{
            'id': c.id,
            'name': c.name,
            'email': c.email,
            'phone': c.phone,
            'subject': c.subject,
            'message': c.message,
            'status': c.status,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in contacts]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def api_status():
    """API status check"""
    return jsonify({
        'status': 'online',
        'message': 'Kolan Hanmanth Reddy - Political Leader Website API',
        'version': '1.0.0'
    }), 200


# ============================================
# COMMUNITY IMPACT ENDPOINTS
# ============================================

@app.route('/api/community-impacts', methods=['GET'])
def get_community_impacts():
    """Get all community impact items"""
    try:
        # Get limit parameter for pagination
        limit = request.args.get('limit', type=int)
        
        # Query active items ordered by display_order
        query = CommunityImpact.query.filter_by(is_active=True).order_by(CommunityImpact.display_order.asc())
        
        if limit:
            impacts = query.limit(limit).all()
        else:
            impacts = query.all()
            
        data = [impact.to_dict() for impact in impacts]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/community-impacts/all', methods=['GET'])
def get_all_community_impacts():
    """Get all community impact items (including inactive) for admin"""
    try:
        impacts = CommunityImpact.query.order_by(CommunityImpact.display_order.asc()).all()
        data = [impact.to_dict() for impact in impacts]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/community-impacts', methods=['POST'])
def create_community_impact():
    """Create a new community impact item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'badge', 'image_url', 'overlay_title']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create impact ID
        impact_id = f"CI_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Get max display order
        max_order = db.session.query(db.func.max(CommunityImpact.display_order)).scalar() or 0
        
        # Create impact object
        impact = CommunityImpact(
            id=impact_id,
            title=data['title'],
            description=data['description'],
            badge=data['badge'],
            image_url=data['image_url'],
            overlay_title=data['overlay_title'],
            is_active=data.get('is_active', True),
            display_order=data.get('display_order', max_order + 1)
        )
        
        db.session.add(impact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Community impact item created successfully',
            'data': impact.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/community-impacts/<impact_id>', methods=['PUT'])
def update_community_impact(impact_id):
    """Update a community impact item"""
    try:
        impact = CommunityImpact.query.get(impact_id)
        if not impact:
            return jsonify({'success': False, 'message': 'Community impact item not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            impact.title = data['title']
        if 'description' in data:
            impact.description = data['description']
        if 'badge' in data:
            impact.badge = data['badge']
        if 'image_url' in data:
            impact.image_url = data['image_url']
        if 'overlay_title' in data:
            impact.overlay_title = data['overlay_title']
        if 'is_active' in data:
            impact.is_active = data['is_active']
        if 'display_order' in data:
            impact.display_order = data['display_order']
        
        impact.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Community impact item updated successfully',
            'data': impact.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/community-impacts/<impact_id>', methods=['DELETE'])
def delete_community_impact(impact_id):
    """Delete a community impact item"""
    try:
        impact = CommunityImpact.query.get(impact_id)
        if not impact:
            return jsonify({'success': False, 'message': 'Community impact item not found'}), 404
        
        db.session.delete(impact)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Community impact item deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# NEWS ENDPOINTS
# ============================================

@app.route('/api/news', methods=['GET'])
def get_news():
    """Get all news items"""
    try:
        # Get limit parameter for pagination
        limit = request.args.get('limit', type=int)
        
        # Query active items ordered by display_order
        query = News.query.filter_by(is_active=True).order_by(News.display_order.asc())
        
        if limit:
            news_items = query.limit(limit).all()
        else:
            news_items = query.all()
            
        data = [news.to_dict() for news in news_items]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/news/all', methods=['GET'])
def get_all_news():
    """Get all news items (including inactive) for admin"""
    try:
        news_items = News.query.order_by(News.display_order.asc()).all()
        data = [news.to_dict() for news in news_items]
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/news', methods=['POST'])
def create_news():
    """Create a new news item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'news_date']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create news ID
        news_id = f"NEWS_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Get max display order
        max_order = db.session.query(db.func.max(News.display_order)).scalar() or 0
        
        # Create news object
        news = News(
            id=news_id,
            title=data['title'],
            description=data['description'],
            category=data['category'],
            news_date=data['news_date'],
            image_url=data.get('image_url', ''),
            link_url=data.get('link_url', ''),
            is_active=data.get('is_active', True),
            display_order=data.get('display_order', max_order + 1)
        )
        
        db.session.add(news)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'News item created successfully',
            'data': news.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/news/<news_id>', methods=['PUT'])
def update_news(news_id):
    """Update a news item"""
    try:
        news = News.query.get(news_id)
        if not news:
            return jsonify({'success': False, 'message': 'News item not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            news.title = data['title']
        if 'description' in data:
            news.description = data['description']
        if 'category' in data:
            news.category = data['category']
        if 'news_date' in data:
            news.news_date = data['news_date']
        if 'image_url' in data:
            news.image_url = data['image_url']
        if 'link_url' in data:
            news.link_url = data['link_url']
        if 'is_active' in data:
            news.is_active = data['is_active']
        if 'display_order' in data:
            news.display_order = data['display_order']
        
        news.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'News item updated successfully',
            'data': news.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/news/<news_id>', methods=['DELETE'])
def delete_news(news_id):
    """Delete a news item"""
    try:
        news = News.query.get(news_id)
        if not news:
            return jsonify({'success': False, 'message': 'News item not found'}), 404
        
        db.session.delete(news)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'News item deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# MEDIA & RECOGNITION API ENDPOINTS
# ============================================

@app.route('/api/media', methods=['GET'])
def get_media():
    """Get media items with optional limit"""
    try:
        limit = request.args.get('limit', type=int)
        query = MediaRecognition.query.filter_by(is_active=True).order_by(MediaRecognition.display_order.asc())
        
        if limit:
            media_items = query.limit(limit).all()
        else:
            media_items = query.all()
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in media_items]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/media/all', methods=['GET'])
def get_all_media():
    """Get all media items including inactive"""
    try:
        media_items = MediaRecognition.query.order_by(MediaRecognition.display_order.asc()).all()
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in media_items]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/media', methods=['POST'])
def create_media():
    """Create a new media item"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'description', 'icon', 'link_url', 'media_type']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        media_id = f"MEDIA_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        max_order = db.session.query(db.func.max(MediaRecognition.display_order)).scalar() or 0
        
        media = MediaRecognition(
            id=media_id,
            title=data['title'],
            description=data['description'],
            icon=data['icon'],
            link_url=data['link_url'],
            link_text=data.get('link_text', 'Read Article'),
            media_type=data['media_type'],
            is_active=data.get('is_active', True),
            display_order=data.get('display_order', max_order + 1)
        )
        
        db.session.add(media)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Media item created successfully',
            'data': media.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/media/<media_id>', methods=['PUT'])
def update_media(media_id):
    """Update a media item"""
    try:
        media = MediaRecognition.query.get(media_id)
        if not media:
            return jsonify({'success': False, 'message': 'Media item not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            media.title = data['title']
        if 'description' in data:
            media.description = data['description']
        if 'icon' in data:
            media.icon = data['icon']
        if 'link_url' in data:
            media.link_url = data['link_url']
        if 'link_text' in data:
            media.link_text = data['link_text']
        if 'media_type' in data:
            media.media_type = data['media_type']
        if 'is_active' in data:
            media.is_active = data['is_active']
        if 'display_order' in data:
            media.display_order = data['display_order']
        
        media.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Media item updated successfully',
            'data': media.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/media/<media_id>', methods=['DELETE'])
def delete_media(media_id):
    """Delete a media item"""
    try:
        media = MediaRecognition.query.get(media_id)
        if not media:
            return jsonify({'success': False, 'message': 'Media item not found'}), 404
        
        db.session.delete(media)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Media item deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# TESTIMONIALS API ENDPOINTS
# ============================================

@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    """Get testimonials with optional limit"""
    try:
        limit = request.args.get('limit', type=int)
        query = Testimonial.query.filter_by(is_active=True).order_by(Testimonial.display_order.asc())
        
        if limit:
            testimonials = query.limit(limit).all()
        else:
            testimonials = query.all()
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in testimonials]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/testimonials/all', methods=['GET'])
def get_all_testimonials():
    """Get all testimonials including inactive"""
    try:
        testimonials = Testimonial.query.order_by(Testimonial.display_order.asc()).all()
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in testimonials]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/testimonials', methods=['POST'])
def create_testimonial():
    """Create a new testimonial"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'designation', 'location', 'testimonial_text']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        testimonial_id = f"TEST_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        max_order = db.session.query(db.func.max(Testimonial.display_order)).scalar() or 0
        
        testimonial = Testimonial(
            id=testimonial_id,
            name=data['name'],
            designation=data['designation'],
            location=data['location'],
            testimonial_text=data['testimonial_text'],
            rating=data.get('rating', 5),
            avatar_icon=data.get('avatar_icon', 'fas fa-user'),
            is_active=data.get('is_active', True),
            display_order=data.get('display_order', max_order + 1)
        )
        
        db.session.add(testimonial)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Testimonial created successfully',
            'data': testimonial.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/testimonials/<testimonial_id>', methods=['PUT'])
def update_testimonial(testimonial_id):
    """Update a testimonial"""
    try:
        testimonial = Testimonial.query.get(testimonial_id)
        if not testimonial:
            return jsonify({'success': False, 'message': 'Testimonial not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            testimonial.name = data['name']
        if 'designation' in data:
            testimonial.designation = data['designation']
        if 'location' in data:
            testimonial.location = data['location']
        if 'testimonial_text' in data:
            testimonial.testimonial_text = data['testimonial_text']
        if 'rating' in data:
            testimonial.rating = data['rating']
        if 'avatar_icon' in data:
            testimonial.avatar_icon = data['avatar_icon']
        if 'is_active' in data:
            testimonial.is_active = data['is_active']
        if 'display_order' in data:
            testimonial.display_order = data['display_order']
        
        testimonial.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Testimonial updated successfully',
            'data': testimonial.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/testimonials/<testimonial_id>', methods=['DELETE'])
def delete_testimonial(testimonial_id):
    """Delete a testimonial"""
    try:
        testimonial = Testimonial.query.get(testimonial_id)
        if not testimonial:
            return jsonify({'success': False, 'message': 'Testimonial not found'}), 404
        
        db.session.delete(testimonial)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Testimonial deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# GALLERY API ENDPOINTS (Photos & Videos)
# ============================================

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Get gallery items with optional filtering by type and limit"""
    try:
        media_type = request.args.get('type')  # 'photo' or 'video'
        limit = request.args.get('limit', type=int)
        
        query = Gallery.query.filter_by(is_active=True)
        
        if media_type:
            query = query.filter_by(media_type=media_type)
        
        query = query.order_by(Gallery.display_order.asc())
        
        if limit:
            gallery_items = query.limit(limit).all()
        else:
            gallery_items = query.all()
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in gallery_items]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/gallery/all', methods=['GET'])
def get_all_gallery():
    """Get all gallery items including inactive"""
    try:
        media_type = request.args.get('type')  # Optional filter
        
        query = Gallery.query
        
        if media_type:
            query = query.filter_by(media_type=media_type)
        
        gallery_items = query.order_by(Gallery.display_order.asc()).all()
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in gallery_items]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/gallery', methods=['POST'])
def create_gallery_item():
    """Create a new gallery item"""
    try:
        data = request.get_json()
        
        required_fields = ['title', 'media_url', 'media_type']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        if data['media_type'] not in ['photo', 'video']:
            return jsonify({'success': False, 'message': 'Invalid media_type. Use "photo" or "video"'}), 400
        
        gallery_id = f"GALLERY_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        max_order = db.session.query(db.func.max(Gallery.display_order)).scalar() or 0
        
        gallery = Gallery(
            id=gallery_id,
            title=data['title'],
            description=data.get('description', ''),
            media_url=data['media_url'],
            media_type=data['media_type'],
            thumbnail_url=data.get('thumbnail_url', ''),
            video_embed_url=data.get('video_embed_url', ''),
            is_active=data.get('is_active', True),
            display_order=data.get('display_order', max_order + 1)
        )
        
        db.session.add(gallery)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gallery item created successfully',
            'data': gallery.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/gallery/<gallery_id>', methods=['PUT'])
def update_gallery_item(gallery_id):
    """Update a gallery item"""
    try:
        gallery = Gallery.query.get(gallery_id)
        if not gallery:
            return jsonify({'success': False, 'message': 'Gallery item not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            gallery.title = data['title']
        if 'description' in data:
            gallery.description = data['description']
        if 'media_url' in data:
            gallery.media_url = data['media_url']
        if 'media_type' in data:
            if data['media_type'] not in ['photo', 'video']:
                return jsonify({'success': False, 'message': 'Invalid media_type'}), 400
            gallery.media_type = data['media_type']
        if 'thumbnail_url' in data:
            gallery.thumbnail_url = data['thumbnail_url']
        if 'video_embed_url' in data:
            gallery.video_embed_url = data['video_embed_url']
        if 'is_active' in data:
            gallery.is_active = data['is_active']
        if 'display_order' in data:
            gallery.display_order = data['display_order']
        
        gallery.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gallery item updated successfully',
            'data': gallery.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/gallery/<gallery_id>', methods=['DELETE'])
def delete_gallery_item(gallery_id):
    """Delete a gallery item"""
    try:
        gallery = Gallery.query.get(gallery_id)
        if not gallery:
            return jsonify({'success': False, 'message': 'Gallery item not found'}), 404
        
        db.session.delete(gallery)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gallery item deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
# TEST EMAIL ENDPOINT (for debugging)
# ============================================

@app.route('/api/test-email', methods=['POST'])
def test_email():
    """Test email configuration by sending a test email"""
    try:
        data = request.get_json()
        recipient = data.get('email', app.config['MAIL_USERNAME'])
        
        msg = Message(
            subject='Test Email - KHR Website',
            recipients=[recipient],
            html="""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #ff9500;">Email Configuration Test</h2>
                    <p>This is a test email from the Kolan Hanmanth Reddy website.</p>
                    <p>If you receive this email, your SMTP configuration is working correctly!</p>
                    <p style="margin-top: 30px; color: #666;">
                        Best regards,<br>
                        KHR Website
                    </p>
                </body>
            </html>
            """
        )
        
        mail.send(msg)
        
        return jsonify({
            'success': True,
            'message': f'Test email sent successfully to {recipient}'
        }), 200
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("=" * 50)
        print("EMAIL ERROR:")
        print(error_details)
        print("=" * 50)
        return jsonify({
            'success': False,
            'message': f'Failed to send email: {str(e)}',
            'details': error_details
        }), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'success': False, 'message': 'Internal server error'}), 500


# ============================================
# DATABASE INITIALIZATION
# ============================================

def init_db():
    """Initialize database and create default admin user"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if default admin user exists
        admin_username = os.getenv('ADMIN_USERNAME', 'khr')
        admin_password = os.getenv('ADMIN_PASSWORD', 'khr@123')
        admin = AdminUser.query.filter_by(username=admin_username).first()
        if not admin:
            # Create default admin user
            admin = AdminUser()
            admin.id = 'admin_001'
            admin.username = admin_username
            admin.email = os.getenv('ADMIN_EMAIL', 'admin@kolanhanmanthreddy.com')
            admin.set_password(admin_password)
            admin.role = 'admin'
            admin.is_active = True
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created successfully!")
            print(f"Username: {admin_username}")
            print(f"Password: {admin_password}")
        else:
            print("Admin user already exists!")


# ============================================
# AI CHAT API
# ============================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI Chat endpoint using Groq"""
    if groq_client is None:
        return jsonify({'success': False, 'message': 'AI service not configured. Please contact administrator.'}), 503
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'success': False, 'message': 'Message is required'}), 400
        
        # Load knowledge base from file
        knowledge_base_path = os.path.join(os.path.dirname(__file__), 'khr_knowledge_base.txt')
        try:
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                knowledge_base = f.read()
        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            knowledge_base = "Knowledge base not available."
        
        # System prompt with comprehensive information from knowledge base
        system_prompt = f"""You are an AI assistant specifically designed to answer questions about Kolan Hanmanth Reddy, a political leader from Telangana, India. 

CRITICAL RESTRICTION - MUST FOLLOW:
⚠️ ABSOLUTE MAXIMUM: 300 WORDS PER RESPONSE - NO EXCEPTIONS! Count your words and STOP at 300 words maximum. This is mandatory.

IMPORTANT RULES:
1. ONLY answer questions related to Kolan Hanmanth Reddy, his work, vision, political career, constituency, initiatives, or related topics
2. If a question is NOT related to Kolan Hanmanth Reddy, politely respond with a friendly message like: "I'm specialized in providing information about Kolan Hanmanth Reddy and his work. Please feel free to ask me anything about his political career, vision, initiatives, or constituency work!"
3. Be friendly, professional, conversational, and informative
4. Provide accurate information ONLY from the knowledge base below
5. If information is not in the knowledge base, acknowledge that you don't have that specific detail but offer related information if available
6. Use natural, conversational language - avoid being too formal or robotic
7. For questions about his political journey/timeline/career, provide detailed chronological information from the knowledge base but stay within 300 words
8. FORMAT RESPONSES IN BULLET POINTS for easy reading:
   - Start with a brief intro sentence if needed
   - Use bullet points (•) for main information
   - Use sub-bullets or numbered lists for detailed timelines
   - Keep each bullet point concise and clear
   - Example format:
     Here's information about X:
     • First key point
     • Second key point
     • Third key point

COMPLETE KNOWLEDGE BASE ABOUT KOLAN HANMANTH REDDY:

{knowledge_base}

Remember: Use ONLY the information from the knowledge base above. Be accurate, helpful, and conversational. If someone asks about his political journey, provide the detailed timeline with years and positions held.
"""
        
        # Build messages for Groq API
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (limit to last 10 exchanges to manage context)
        if conversation_history:
            recent_history = conversation_history[-20:]  # Last 10 exchanges (user + assistant)
            messages.extend(recent_history)
        
        # Generate response using Groq
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=350,  # Strictly limit to ~300 words maximum
                top_p=0.9,
                stream=False
            )
            
            response_content = completion.choices[0].message.content.strip()
            
            return jsonify({
                'success': True,
                'response': response_content
            }), 200
            
        except Exception as groq_error:
            print(f"Groq API Error: {str(groq_error)}")
            return jsonify({
                'success': False,
                'message': 'AI service temporarily unavailable. Please try again.'
            }), 500
        
    except Exception as e:
        print(f"Chat Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred processing your request.'
        }), 500


# Initialize database when app starts (works with both gunicorn and direct run)
try:
    init_db()
except Exception as e:
    print(f"WARNING: Database initialization error: {e}")
    print("App will still start - database may need manual initialization.")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
