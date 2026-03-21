"""
Form submission endpoints:
  POST /api/complaint
  POST /api/feedback
  POST /api/skills-registration
  POST /api/contact
"""

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from ..database import get_db
from ..models import Complaint, Feedback, SkillsRegistration, Contact
from ..schemas import ComplaintCreate, FeedbackCreate, SkillsCreate, ContactCreate
from ..email_utils import (
    send_complaint_confirmation_email,
    send_feedback_confirmation_email,
    send_skills_confirmation_email,
    send_contact_confirmation_email,
)

router = APIRouter()


@router.post('/api/complaint', status_code=201)
async def submit_complaint(
    data: ComplaintCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        complaint_id = f"COMP_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        count = db.query(func.count(Complaint.id)).scalar() or 0
        ref_number = f"REF-{datetime.utcnow().year}-{count + 1:05d}"

        complaint = Complaint(
            id=complaint_id,
            name=data.name,
            phone=data.phone,
            email=data.email,
            area=data.area,
            category=data.category,
            subject=data.subject,
            message=data.message,
            address=data.address,
            reference_number=ref_number,
        )
        db.add(complaint)
        db.commit()
        db.refresh(complaint)

        background_tasks.add_task(
            send_complaint_confirmation_email,
            {
                'email': complaint.email,
                'name': complaint.name,
                'reference_number': complaint.reference_number,
                'category': complaint.category,
                'subject': complaint.subject,
            },
        )

        return {
            'success': True,
            'message': 'Complaint submitted successfully',
            'reference_number': ref_number,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/feedback', status_code=201)
async def submit_feedback(
    data: FeedbackCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail='Rating must be between 1 and 5')
    try:
        feedback_id = f"FB_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        feedback = Feedback(
            id=feedback_id,
            name=data.name,
            email=data.email,
            phone=data.phone or '',
            category=data.category,
            rating=data.rating,
            message=data.message,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        background_tasks.add_task(
            send_feedback_confirmation_email,
            {
                'email': feedback.email,
                'name': feedback.name,
                'category': feedback.category,
                'rating': feedback.rating,
            },
        )

        return {'success': True, 'message': 'Thank you for your feedback!'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/skills-registration', status_code=201)
async def register_skills(
    data: SkillsCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        registration_id = f"SKL_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        dob = datetime.strptime(data.dob, '%Y-%m-%d').date()

        registration = SkillsRegistration(
            id=registration_id,
            name=data.name,
            phone=data.phone,
            email=data.email,
            dob=dob,
            education=data.education,
            institution=data.institution or '',
            location=data.location,
            city=data.city,
            motivation=data.motivation,
            confirmation_sent=True,
        )
        db.add(registration)
        db.commit()
        db.refresh(registration)

        background_tasks.add_task(
            send_skills_confirmation_email,
            {
                'email': registration.email,
                'name': registration.name,
                'education': registration.education,
                'location': registration.location,
            },
        )

        return {'success': True, 'message': 'Registration successful! Confirmation email sent.'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/contact', status_code=201)
async def submit_contact(
    data: ContactCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    try:
        contact_id = f"CNT_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        contact = Contact(
            id=contact_id,
            name=data.name,
            email=data.email,
            phone=data.phone or '',
            subject=data.subject,
            message=data.message,
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)

        background_tasks.add_task(
            send_contact_confirmation_email,
            {
                'email': contact.email,
                'name': contact.name,
                'subject': contact.subject,
            },
        )

        return {'success': True, 'message': 'Message sent successfully!'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
