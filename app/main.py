# =========================
# Dependencies
# =========================

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
import json
import os

from config.dynamic import dynamic
from routes import analytics, fallback, templates
from routes.fallback import error_page

# =========================
# FastAPI
# =========================

app = FastAPI()
app.include_router(analytics.router)
app.include_router(fallback.router)
app.include_router(templates.router)

# -------------------------

app.mount(
    '/static',
    StaticFiles(
        directory=os.path.join(os.path.dirname(__file__), 'static')
    ), name='static'
)
app.mount(
    '/data/templates',
    StaticFiles(
        directory=os.path.join(os.path.dirname(__file__), 'data/templates')
    ),
    name='data-templates'
)

# =========================
# Configurations
# =========================

config_path = os.path.join(
    os.path.dirname(__file__), 'config', 'static.json'
)
with open(config_path) as f:
    static = json.load(f)
config = {
    **static,
    **dynamic
}

@app.middleware('http')
async def add_config_to_request(request: Request, call_next):
    request.state.config = config
    response = await call_next(request)
    return response

async def handle_exception(request: Request, exc: Exception):
    return error_page(request, exc)

app.add_exception_handler(Exception, handle_exception)
app.add_exception_handler(HTTPException, handle_exception)
app.add_exception_handler(StarletteHTTPException, handle_exception)
