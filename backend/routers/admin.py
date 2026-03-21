"""
Admin data-retrieval endpoints (read-only list views):
  GET /api/complaints
  GET /api/feedback-list
  GET /api/skills-list
  GET /api/contacts-list
  GET /api/status
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Complaint, Feedback, SkillsRegistration, Contact

router = APIRouter()


@router.get('/api/status')
def api_status():
    return {
        'status': 'online',
        'message': 'Kolan Hanmanth Reddy - Political Leader Website API',
        'version': '1.0.0',
    }


@router.get('/api/complaints')
def get_complaints(db: Session = Depends(get_db)):
    try:
        complaints = db.query(Complaint).all()
        data = [
            {
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
                'created_at': c.created_at.isoformat() if c.created_at else None,
            }
            for c in complaints
        ]
        return {'success': True, 'data': data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/feedback-list')
def get_feedback_list(db: Session = Depends(get_db)):
    try:
        feedbacks = db.query(Feedback).all()
        data = [
            {
                'id': f.id,
                'name': f.name,
                'email': f.email,
                'phone': f.phone,
                'category': f.category,
                'rating': f.rating,
                'message': f.message,
                'status': f.status,
                'created_at': f.created_at.isoformat() if f.created_at else None,
            }
            for f in feedbacks
        ]
        return {'success': True, 'data': data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/skills-list')
def get_skills_list(db: Session = Depends(get_db)):
    try:
        registrations = db.query(SkillsRegistration).all()
        data = [
            {
                'id': r.id,
                'name': r.name,
                'email': r.email,
                'phone': r.phone,
                'dob': r.dob.isoformat() if r.dob else None,
                'education': r.education,
                'institution': r.institution,
                'location': r.location,
                'city': r.city,
                'motivation': r.motivation,
                'status': r.status,
                'created_at': r.created_at.isoformat() if r.created_at else None,
            }
            for r in registrations
        ]
        return {'success': True, 'data': data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/contacts-list')
def get_contacts_list(db: Session = Depends(get_db)):
    try:
        contacts = db.query(Contact).all()
        data = [
            {
                'id': c.id,
                'name': c.name,
                'email': c.email,
                'phone': c.phone,
                'subject': c.subject,
                'message': c.message,
                'status': c.status,
                'created_at': c.created_at.isoformat() if c.created_at else None,
            }
            for c in contacts
        ]
        return {'success': True, 'data': data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
