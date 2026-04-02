# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

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

    template = 'pages/documentation.html'
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

# @router.get('/maintenance', name='templates:maintenance')
# async def maintenance(request: Request):

#     # Request Logging
#     log_request(request)

#     # -------------------------

#     template = 'pages/maintenance.html'
#     logger.debug(f"Rendering template: {template}")

#     # -------------------------

#     logger.info(f"[200] {request.url.path}")
#     return jinja_templates.TemplateResponse(
#         template,
#         {
#             'request': request,
#             'config': request.state.config
#         }
#     )
