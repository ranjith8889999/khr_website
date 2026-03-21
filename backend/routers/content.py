"""
CRUD endpoints for all content types:
  Community Impacts, News, Media Recognition, Testimonials, Gallery

IMPORTANT – route ordering rules in FastAPI/Starlette:
  Routes with literal path segments (e.g. /api/news/all) are registered
  BEFORE parameterised ones (e.g. /api/news/{id}) so they match first.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from ..database import get_db
from ..models import CommunityImpact, News, MediaRecognition, Testimonial, Gallery
from ..schemas import (
    CommunityImpactCreate, CommunityImpactUpdate,
    NewsCreate, NewsUpdate,
    MediaCreate, MediaUpdate,
    TestimonialCreate, TestimonialUpdate,
    GalleryCreate, GalleryUpdate,
)

router = APIRouter()


# ── Community Impacts ─────────────────────────────────────────────────

@router.get('/api/community-impacts/all')
def get_all_community_impacts(db: Session = Depends(get_db)):
    try:
        impacts = db.query(CommunityImpact).order_by(CommunityImpact.display_order.asc()).all()
        return {'success': True, 'data': [i.to_dict() for i in impacts]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/community-impacts')
def get_community_impacts(limit: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = (
            db.query(CommunityImpact)
            .filter(CommunityImpact.is_active == True)
            .order_by(CommunityImpact.display_order.asc())
        )
        impacts = query.limit(limit).all() if limit else query.all()
        return {'success': True, 'data': [i.to_dict() for i in impacts]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/community-impacts', status_code=201)
def create_community_impact(data: CommunityImpactCreate, db: Session = Depends(get_db)):
    try:
        impact_id = f"CI_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        max_order = db.query(func.max(CommunityImpact.display_order)).scalar() or 0
        impact = CommunityImpact(
            id=impact_id,
            title=data.title,
            description=data.description,
            badge=data.badge,
            image_url=data.image_url,
            overlay_title=data.overlay_title,
            is_active=data.is_active,
            display_order=data.display_order if data.display_order is not None else max_order + 1,
        )
        db.add(impact)
        db.commit()
        db.refresh(impact)
        return {'success': True, 'message': 'Community impact item created successfully', 'data': impact.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/api/community-impacts/{impact_id}')
def update_community_impact(impact_id: str, data: CommunityImpactUpdate, db: Session = Depends(get_db)):
    impact = db.query(CommunityImpact).filter(CommunityImpact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail='Community impact item not found')
    try:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(impact, field, value)
        impact.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(impact)
        return {'success': True, 'message': 'Community impact item updated successfully', 'data': impact.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/api/community-impacts/{impact_id}')
def delete_community_impact(impact_id: str, db: Session = Depends(get_db)):
    impact = db.query(CommunityImpact).filter(CommunityImpact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail='Community impact item not found')
    try:
        db.delete(impact)
        db.commit()
        return {'success': True, 'message': 'Community impact item deleted successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── News ──────────────────────────────────────────────────────────────
# /api/news/all MUST come before /api/news/{news_id}

@router.get('/api/news/all')
def get_all_news(db: Session = Depends(get_db)):
    try:
        items = db.query(News).order_by(News.display_order.asc()).all()
        return {'success': True, 'data': [n.to_dict() for n in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/news')
def get_news(limit: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(News).filter(News.is_active == True).order_by(News.display_order.asc())
        items = query.limit(limit).all() if limit else query.all()
        return {'success': True, 'data': [n.to_dict() for n in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/news', status_code=201)
def create_news(data: NewsCreate, db: Session = Depends(get_db)):
    try:
        news_id = f"NEWS_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        max_order = db.query(func.max(News.display_order)).scalar() or 0
        news = News(
            id=news_id,
            title=data.title,
            description=data.description,
            category=data.category,
            news_date=data.news_date,
            image_url=data.image_url or '',
            link_url=data.link_url or '',
            is_active=data.is_active,
            display_order=data.display_order if data.display_order is not None else max_order + 1,
        )
        db.add(news)
        db.commit()
        db.refresh(news)
        return {'success': True, 'message': 'News item created successfully', 'data': news.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/api/news/{news_id}')
def update_news(news_id: str, data: NewsUpdate, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail='News item not found')
    try:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(news, field, value)
        news.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(news)
        return {'success': True, 'message': 'News item updated successfully', 'data': news.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/api/news/{news_id}')
def delete_news(news_id: str, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail='News item not found')
    try:
        db.delete(news)
        db.commit()
        return {'success': True, 'message': 'News item deleted successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── Media Recognition ─────────────────────────────────────────────────
# /api/media/all MUST come before /api/media/{media_id}

@router.get('/api/media/all')
def get_all_media(db: Session = Depends(get_db)):
    try:
        items = db.query(MediaRecognition).order_by(MediaRecognition.display_order.asc()).all()
        return {'success': True, 'data': [m.to_dict() for m in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/media')
def get_media(limit: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = (
            db.query(MediaRecognition)
            .filter(MediaRecognition.is_active == True)
            .order_by(MediaRecognition.display_order.asc())
        )
        items = query.limit(limit).all() if limit else query.all()
        return {'success': True, 'data': [m.to_dict() for m in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/media', status_code=201)
def create_media(data: MediaCreate, db: Session = Depends(get_db)):
    try:
        media_id = f"MEDIA_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        max_order = db.query(func.max(MediaRecognition.display_order)).scalar() or 0
        media = MediaRecognition(
            id=media_id,
            title=data.title,
            description=data.description,
            icon=data.icon,
            link_url=data.link_url,
            link_text=data.link_text or 'Read Article',
            media_type=data.media_type,
            is_active=data.is_active,
            display_order=data.display_order if data.display_order is not None else max_order + 1,
        )
        db.add(media)
        db.commit()
        db.refresh(media)
        return {'success': True, 'message': 'Media item created successfully', 'data': media.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/api/media/{media_id}')
def update_media(media_id: str, data: MediaUpdate, db: Session = Depends(get_db)):
    media = db.query(MediaRecognition).filter(MediaRecognition.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail='Media item not found')
    try:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(media, field, value)
        media.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(media)
        return {'success': True, 'message': 'Media item updated successfully', 'data': media.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/api/media/{media_id}')
def delete_media(media_id: str, db: Session = Depends(get_db)):
    media = db.query(MediaRecognition).filter(MediaRecognition.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail='Media item not found')
    try:
        db.delete(media)
        db.commit()
        return {'success': True, 'message': 'Media item deleted successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── Testimonials ──────────────────────────────────────────────────────
# /api/testimonials/all MUST come before /api/testimonials/{id}

@router.get('/api/testimonials/all')
def get_all_testimonials(db: Session = Depends(get_db)):
    try:
        items = db.query(Testimonial).order_by(Testimonial.display_order.asc()).all()
        return {'success': True, 'data': [t.to_dict() for t in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/testimonials')
def get_testimonials(limit: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = (
            db.query(Testimonial)
            .filter(Testimonial.is_active == True)
            .order_by(Testimonial.display_order.asc())
        )
        items = query.limit(limit).all() if limit else query.all()
        return {'success': True, 'data': [t.to_dict() for t in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/testimonials', status_code=201)
def create_testimonial(data: TestimonialCreate, db: Session = Depends(get_db)):
    try:
        tid = f"TEST_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        max_order = db.query(func.max(Testimonial.display_order)).scalar() or 0
        testimonial = Testimonial(
            id=tid,
            name=data.name,
            designation=data.designation,
            location=data.location,
            testimonial_text=data.testimonial_text,
            rating=data.rating,
            avatar_icon=data.avatar_icon,
            is_active=data.is_active,
            display_order=data.display_order if data.display_order is not None else max_order + 1,
        )
        db.add(testimonial)
        db.commit()
        db.refresh(testimonial)
        return {'success': True, 'message': 'Testimonial created successfully', 'data': testimonial.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/api/testimonials/{testimonial_id}')
def update_testimonial(testimonial_id: str, data: TestimonialUpdate, db: Session = Depends(get_db)):
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(status_code=404, detail='Testimonial not found')
    try:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(testimonial, field, value)
        testimonial.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(testimonial)
        return {'success': True, 'message': 'Testimonial updated successfully', 'data': testimonial.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/api/testimonials/{testimonial_id}')
def delete_testimonial(testimonial_id: str, db: Session = Depends(get_db)):
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(status_code=404, detail='Testimonial not found')
    try:
        db.delete(testimonial)
        db.commit()
        return {'success': True, 'message': 'Testimonial deleted successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ── Gallery ───────────────────────────────────────────────────────────
# /api/gallery/all MUST come before /api/gallery/{gallery_id}

@router.get('/api/gallery/all')
def get_all_gallery(type: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Gallery)
        if type:
            query = query.filter(Gallery.media_type == type)
        items = query.order_by(Gallery.display_order.asc()).all()
        return {'success': True, 'data': [g.to_dict() for g in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/gallery')
def get_gallery(type: Optional[str] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Gallery).filter(Gallery.is_active == True)
        if type:
            query = query.filter(Gallery.media_type == type)
        query = query.order_by(Gallery.display_order.asc())
        items = query.limit(limit).all() if limit else query.all()
        return {'success': True, 'data': [g.to_dict() for g in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/gallery', status_code=201)
def create_gallery_item(data: GalleryCreate, db: Session = Depends(get_db)):
    if data.media_type not in ['photo', 'video']:
        raise HTTPException(status_code=400, detail='Invalid media_type. Use "photo" or "video"')
    try:
        gid = f"GALLERY_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
        max_order = db.query(func.max(Gallery.display_order)).scalar() or 0
        gallery = Gallery(
            id=gid,
            title=data.title,
            description=data.description or '',
            media_url=data.media_url,
            media_type=data.media_type,
            thumbnail_url=data.thumbnail_url or '',
            video_embed_url=data.video_embed_url or '',
            is_active=data.is_active,
            display_order=data.display_order if data.display_order is not None else max_order + 1,
        )
        db.add(gallery)
        db.commit()
        db.refresh(gallery)
        return {'success': True, 'message': 'Gallery item created successfully', 'data': gallery.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put('/api/gallery/{gallery_id}')
def update_gallery_item(gallery_id: str, data: GalleryUpdate, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail='Gallery item not found')
    try:
        update_data = data.model_dump(exclude_none=True)
        if 'media_type' in update_data and update_data['media_type'] not in ['photo', 'video']:
            raise HTTPException(status_code=400, detail='Invalid media_type. Use "photo" or "video"')
        for field, value in update_data.items():
            setattr(gallery, field, value)
        gallery.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(gallery)
        return {'success': True, 'message': 'Gallery item updated successfully', 'data': gallery.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/api/gallery/{gallery_id}')
def delete_gallery_item(gallery_id: str, db: Session = Depends(get_db)):
    gallery = db.query(Gallery).filter(Gallery.id == gallery_id).first()
    if not gallery:
        raise HTTPException(status_code=404, detail='Gallery item not found')
    try:
        db.delete(gallery)
        db.commit()
        return {'success': True, 'message': 'Gallery item deleted successfully'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
