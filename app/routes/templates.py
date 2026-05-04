# =========================
# Dependencies
# =========================

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from http import HTTPStatus

from api import model as model_api
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

    # Template
    template = 'pages/home.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )

@router.get('/analytics/templates', name='templates:analytics_templates')
def analytics_templates(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    # Template
    template = 'pages/analytics-templates.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )

@router.get('/analytics', name='templates:analytics')
def analytics(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    # Template
    template = 'pages/analytics.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG
        }
    )

@router.get('/ai/model/overview', name='templates:model_overview')
def model_overview(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    # Template
    template = 'pages/model-overview.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG,
            'model_html': request.app.state.model_html,
            'model_metadata': request.app.state.model_metadata,
            'model_registry': request.app.state.model_registry
        }
    )

@router.get('/ai/model/performance', name='templates:model_performance')
def model_performance(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    # Template
    template = 'pages/model-performance.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    # Badges
    badges = model_api.get_badges(
        request.app.state.model_metadata
    )

    # Plot EUI Distribution
    plot_eui_dist = model_api.get_plot_eui_dist(request)

    # Plot Heatmap
    plot_heatmap = model_api.get_plot_heatmap(request)

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG,
            'model_metadata': request.app.state.model_metadata,
            'badges': badges,
            'plot_eui_dist': plot_eui_dist,
            'plot_heatmap': plot_heatmap,
        }
    )

@router.get('/resources/documentation', name='templates:documentation')
def documentation(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return RedirectResponse(url='https://docs.robertovicario.com/energyplus-ai')

@router.get('/resources/api-reference', name='templates:api_reference')
def api_reference(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return RedirectResponse(url='https://docs.robertovicario.com/energyplus-ai/api-reference')

@router.get('/resources/changelog', name='templates:changelog')
def changelog(request: Request):

    # Request Logging
    log_request(request)

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return RedirectResponse(url='https://docs.robertovicario.com/energyplus-ai/changelog')

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

    # Template
    template = 'pages/error.html'
    logger.debug(f"Rendering template: {template}")

    # -------------------------

    logger.info(f"[200] {request.url.path}")
    return jinja_templates.TemplateResponse(
        template,
        {
            'request': request,
            'config': request.app.state.CONFIG,
            'err_code': err_code,
            'err_name': err_name,
            'err_desc': err_desc,
        },
    )
