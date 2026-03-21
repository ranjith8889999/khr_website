"""
Pydantic request-body schemas for all API endpoints.
"""

from pydantic import BaseModel
from typing import Optional, List, Any


# ── Form Submissions ──────────────────────────────────────────────────

class ComplaintCreate(BaseModel):
    name: str
    phone: str
    email: str
    area: str
    category: str
    subject: str
    message: str
    address: str


class FeedbackCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ''
    category: str
    rating: int
    message: str


class SkillsCreate(BaseModel):
    name: str
    phone: str
    email: str
    dob: str          # 'YYYY-MM-DD'
    education: str
    institution: Optional[str] = ''
    location: str
    city: str
    motivation: str


class ContactCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ''
    subject: str
    message: str


# ── Community Impacts ─────────────────────────────────────────────────

class CommunityImpactCreate(BaseModel):
    title: str
    description: str
    badge: str
    image_url: str
    overlay_title: str
    is_active: Optional[bool] = True
    display_order: Optional[int] = None


class CommunityImpactUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    badge: Optional[str] = None
    image_url: Optional[str] = None
    overlay_title: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


# ── News ──────────────────────────────────────────────────────────────

class NewsCreate(BaseModel):
    title: str
    description: str
    category: str
    news_date: str
    image_url: Optional[str] = ''
    link_url: Optional[str] = ''
    is_active: Optional[bool] = True
    display_order: Optional[int] = None


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    news_date: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


# ── Media ─────────────────────────────────────────────────────────────

class MediaCreate(BaseModel):
    title: str
    description: str
    icon: str
    link_url: str
    link_text: Optional[str] = 'Read Article'
    media_type: str
    is_active: Optional[bool] = True
    display_order: Optional[int] = None


class MediaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    link_url: Optional[str] = None
    link_text: Optional[str] = None
    media_type: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


# ── Testimonials ──────────────────────────────────────────────────────

class TestimonialCreate(BaseModel):
    name: str
    designation: str
    location: str
    testimonial_text: str
    rating: Optional[int] = 5
    avatar_icon: Optional[str] = 'fas fa-user'
    is_active: Optional[bool] = True
    display_order: Optional[int] = None


class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    location: Optional[str] = None
    testimonial_text: Optional[str] = None
    rating: Optional[int] = None
    avatar_icon: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


# ── Gallery ───────────────────────────────────────────────────────────

class GalleryCreate(BaseModel):
    title: str
    description: Optional[str] = ''
    media_url: str
    media_type: str       # 'photo' or 'video'
    thumbnail_url: Optional[str] = ''
    video_embed_url: Optional[str] = ''
    is_active: Optional[bool] = True
    display_order: Optional[int] = None


class GalleryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    thumbnail_url: Optional[str] = None
    video_embed_url: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


# ── AI Chat ───────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Any]] = []


# ── Test Email ────────────────────────────────────────────────────────

class TestEmailRequest(BaseModel):
    email: Optional[str] = None
