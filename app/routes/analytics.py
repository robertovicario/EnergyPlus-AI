# =========================
# Dependencies
# =========================

from eppy.modeleditor import IDF
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import JSONResponse
import os
import tempfile
import traceback
import uuid
import zipfile

from api import analytics as this_api
from config.logging import logger, log_request

# =========================
# Configurations
# =========================

# FastAPI
router = APIRouter(prefix='/analytics', tags=['analytics'])

# Progress Tracking
PROGRESS = {}
RESULTS = {}

# EnergyPlus API
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
IDD_FILE = os.path.join(DATA_PATH, 'config', 'Energy+.idd')

# =========================
# Endpoints
# =========================

@router.get('/upload/progress/{job_id}')
async def get_progress(job_id: str):
    return {'progress': PROGRESS.get(job_id, 0)}

@router.post('/upload', name='analytics:upload')
async def upload(
    request: Request,
    file: UploadFile = File(...)
) -> JSONResponse:

    # Request Logging
    log_request(request)

    # -------------------------

    # Progress Tracking
    job_id = str(uuid.uuid4())
    PROGRESS[job_id] = 0

    try:
        with tempfile.TemporaryDirectory() as tmpdir:

            # ZIP
            zip_path = os.path.join(tmpdir, file.filename)
            with open(zip_path, 'wb') as f:
                f.write(await file.read())

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            PROGRESS[job_id] = 20

            # IDF & EPW
            idf_path, epw_path = None, None
            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f.endswith('.idf'):
                        idf_path = os.path.join(root, f)
                    elif f.endswith('.epw'):
                        epw_path = os.path.join(root, f)

            PROGRESS[job_id] = 40

            # Validation
            if not idf_path or not epw_path:
                return JSONResponse(
                    status_code=400,
                    content={'error': 'IDF or EPW file not found in the uploaded ZIP.'}
                )

            IDF.setiddname(IDD_FILE)
            idf = IDF(idf_path, epw_path)
            PROGRESS[job_id] = 60

            # -------------------------

            # Widgets
            widgets = this_api.get_widgets(idf)
            PROGRESS[job_id] = 80

            # Rendering
            rendering = this_api.get_rendering(idf)
            PROGRESS[job_id] = 100

            # -------------------------

            logger.info(f"[200] {request.url.path}")
            return JSONResponse(
                status_code=200,
                content={
                    'job_id': job_id,
                    'widgets': widgets,
                    'rendering': rendering
                }
            )

    # -------------------------

    except Exception:
        tb = traceback.format_exc()
        logger.error(f"[500] {request.url.path}")
        logger.critical(tb)
        return JSONResponse(
            status_code=500,
            content={'error': tb}
        )
