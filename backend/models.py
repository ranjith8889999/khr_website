"""
SQLAlchemy ORM models – shared by all routers via the Base from database.py.
"""

from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, Date
from datetime import datetime
import hashlib

from .database import Base


class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), nullable=False)
    area = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    status = Column(String(20), default='pending')
    reference_number = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_notes = Column(Text, default='')


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    phone = Column(String(20))
    category = Column(String(50), nullable=False)
    rating = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default='received')
    created_at = Column(DateTime, default=datetime.utcnow)


class SkillsRegistration(Base):
    __tablename__ = 'skills_registrations'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(120), nullable=False)
    dob = Column(Date, nullable=False)
    education = Column(String(50), nullable=False)
    institution = Column(String(150))
    location = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    motivation = Column(Text, nullable=False)
    status = Column(String(20), default='pending')
    confirmation_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    phone = Column(String(20))
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(20), default='received')
    created_at = Column(DateTime, default=datetime.utcnow)


class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='moderator')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()


class CommunityImpact(Base):
    __tablename__ = 'community_impacts'

    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    badge = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=False)
    overlay_title = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


class News(Base):
    __tablename__ = 'news'

    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    news_date = Column(String(100), nullable=False)
    image_url = Column(String(500))
    link_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


class MediaRecognition(Base):
    __tablename__ = 'media_recognition'

    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=False)
    link_url = Column(String(500), nullable=False)
    link_text = Column(String(100), default='Read Article')
    media_type = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


class Testimonial(Base):
    __tablename__ = 'testimonials'

    id = Column(String(50), primary_key=True)
    name = Column(String(200), nullable=False)
    designation = Column(String(200), nullable=False)
    location = Column(String(200), nullable=False)
    testimonial_text = Column(Text, nullable=False)
    rating = Column(Integer, default=5)
    avatar_icon = Column(String(50), default='fas fa-user')
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }


class Gallery(Base):
    __tablename__ = 'gallery'

    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    media_url = Column(String(500), nullable=False)
    media_type = Column(String(20), nullable=False)
    thumbnail_url = Column(String(500))
    video_embed_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
