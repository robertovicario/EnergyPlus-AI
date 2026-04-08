# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from http import HTTPStatus

from config.logger import logger, log_request

# =========================
# FastAPI
# =========================

router = APIRouter(prefix='', tags=['templates'])
jinja_templates = Jinja2Templates(directory='templates')

# =========================
# Templates
# =========================

@router.get('/', name='templates:home')
def home(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    template = 'pages/home.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.state.config
        }
    )

@router.get('/analytics', name='templates:analytics')
def analytics(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    template = 'pages/analytics.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.state.config
        }
    )

@router.get('/templates', name='templates:templates')
def templates(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    template = 'pages/templates.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.state.config
        }
    )

@router.get('/documentation', name='templates:documentation')
def documentation(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return RedirectResponse(url='/docs')

@router.get('/changelog', name='templates:changelog')
def changelog(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    template = 'pages/changelog.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.state.config
        }
    )

@router.get('/support', name='templates:support')
def support(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    template = 'pages/support.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.state.config
        }
    )

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

    template = 'pages/error.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.state.config,
            'err_code': err_code,
            'err_name': err_name,
            'err_desc': err_desc,
        },
    )
