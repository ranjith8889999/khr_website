"""
Kolan Hanmanth Reddy - Political Leader Website
FastAPI Backend Application
"""

import os
import sys
import pathlib

# Ensure project root is on sys.path so absolute imports work regardless of
# how this file is launched (direct script, uvicorn reload worker, etc.)
_PROJECT_ROOT = str(pathlib.Path(__file__).parent.parent.resolve())
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# ── Paths ─────────────────────────────────────────────────────────────
# backend/app.py  ->  parent = backend/  ->  parent.parent = project root
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

# Load .env from project root before anything else so env vars are available
# to all modules that import after this point.
load_dotenv(BASE_DIR / '.env')

# ── DB + Models (imported after load_dotenv) ──────────────────────────
from backend.database import engine, SessionLocal  # noqa: E402
from backend.models import Base, AdminUser          # noqa: E402


# ── Database initialisation ───────────────────────────────────────────

def _init_db() -> None:
    """Create all tables and seed the default admin user if absent."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

    db = SessionLocal()
    try:
        admin_username = os.getenv('ADMIN_USERNAME', 'khr')
        admin_password = os.getenv('ADMIN_PASSWORD', 'khr@123')
        admin = db.query(AdminUser).filter(AdminUser.username == admin_username).first()
        if not admin:
            admin = AdminUser(
                id='admin_001',
                username=admin_username,
                email=os.getenv('ADMIN_EMAIL', 'admin@kolanhanmanthreddy.com'),
                role='admin',
                is_active=True,
            )
            admin.set_password(admin_password)
            db.add(admin)
            db.commit()
            print(f"Default admin user created: {admin_username}")
        else:
            print("Admin user already exists!")
    except Exception as e:
        db.rollback()
        print(f"WARNING: Admin user seeding failed: {e}")
    finally:
        db.close()


# ── App lifecycle ─────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        _init_db()
    except Exception as e:
        print(f"WARNING: Database initialisation error: {e}")
        print("App will still start - database may need manual initialisation.")
    yield


# ── FastAPI instance ──────────────────────────────────────────────────

app = FastAPI(
    title='Kolan Hanmanth Reddy – Political Leader Website',
    version='1.0.0',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ── API routers ───────────────────────────────────────────────────────
# Registered FIRST so all /api/* paths are resolved before the static catch-alls.
from backend.routers import admin, chat, content, forms, upload  # noqa: E402

app.include_router(admin.router)
app.include_router(forms.router)
app.include_router(content.router)
app.include_router(upload.router)
app.include_router(chat.router)

# ── Static asset directory mounts ─────────────────────────────────────
# Checked after API routes but before the HTML catch-all.
for _subdir in ('css', 'js', 'images', 'assets', 'data'):
    _dir = BASE_DIR / _subdir
    if _dir.is_dir():
        app.mount(f'/{_subdir}', StaticFiles(directory=str(_dir)), name=_subdir)

# ── HTML / SPA routes ─────────────────────────────────────────────────

@app.get('/', include_in_schema=False)
async def index():
    return FileResponse(str(BASE_DIR / 'index.html'))


@app.get('/admin/{filename:path}', include_in_schema=False)
async def serve_admin(filename: str):
    filepath = BASE_DIR / 'admin' / filename
    if filepath.is_file():
        return FileResponse(str(filepath))
    return JSONResponse({'success': False, 'message': 'Not found'}, status_code=404)


@app.get('/{filename:path}', include_in_schema=False)
async def serve_static(filename: str):
    """Catch-all: serve any project-root file; fall back to index.html for SPA routing."""
    filepath = BASE_DIR / filename
    if filepath.is_file():
        return FileResponse(str(filepath))
    index_path = BASE_DIR / 'index.html'
    if index_path.is_file():
        return FileResponse(str(index_path))
    return JSONResponse({'success': False, 'message': 'Not found'}, status_code=404)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.app:app', host='0.0.0.0', port=8000, reload=True)
