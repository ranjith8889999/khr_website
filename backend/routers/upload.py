"""
Image upload endpoint:  POST /api/upload-image
"""

import pathlib
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

BASE_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
UPLOAD_FOLDER = BASE_DIR / 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

UPLOAD_FOLDER.mkdir(exist_ok=True)


def _allowed(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post('/api/upload-image')
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='No file selected')
    if not _allowed(file.filename):
        raise HTTPException(
            status_code=400,
            detail='File type not allowed. Use: png, jpg, jpeg, gif, webp',
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail='File too large. Maximum 5 MB allowed.')

    ext = file.filename.rsplit('.', 1)[1].lower()
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"community_impact_{timestamp}.{ext}"
    filepath = UPLOAD_FOLDER / filename

    with open(filepath, 'wb') as f:
        f.write(contents)

    return {
        'success': True,
        'message': 'Image uploaded successfully',
        'image_url': f'images/{filename}',
        'filename': filename,
    }
