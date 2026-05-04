# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from config.logger import log_request

# =========================
# Configurations
# =========================

# FastAPI
router = APIRouter(prefix='/ai', tags=['ai'])

# =========================
# Endpoints
# =========================

@router.get('/model/overview/get-model', response_class=HTMLResponse)
def get_model_diagram(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    return request.app.state.model_html

@router.get('/model/performance/get-metadata')
def get_model_performance(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    return request.app.state.model_metadata
