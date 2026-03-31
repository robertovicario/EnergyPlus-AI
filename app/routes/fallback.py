# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from http import HTTPStatus

# =========================
# FastAPI
# =========================

router = APIRouter(prefix='/fallback', tags=['fallback'])
templates = Jinja2Templates(directory='templates')

# =========================
# Templates
# =========================

def error_page(request: Request, error):

    # Information
    err_code = getattr(error, 'status_code', 500)
    try:
        err_name = HTTPStatus(err_code).phrase
        err_desc = HTTPStatus(err_code).description
    except ValueError:
        err_name = type(error).__name__
        err_desc = str(error)

    # -------------------------

    return templates.TemplateResponse(
        'pages/error.html',
        {
            'request': request,
            'config': request.state.config,
            'err_code': err_code,
            'err_name': err_name,
            'err_desc': err_desc,
        },
    )
