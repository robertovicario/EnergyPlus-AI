# =========================
# Dependencies
# =========================

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from functools import lru_cache
from starlette.exceptions import HTTPException as StarletteHTTPException
import json
import os
import pandas as pd

from api import model as model_api
from config.dynamic import dynamic
from routes import (
    analytics,
    model,
    templates
)
from routes.templates import error_page

# =========================
# Configurations
# =========================

# Configurations
CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), 'config', 'static.json'
)
with open(CONFIG_PATH) as f:
    static = json.load(f)
CONFIG = {
    **static,
    **dynamic
}

# Data
DATA_PATH = os.path.join(
    os.path.dirname(__file__), 'data'
)

# Models
MODELS_PATH = os.path.join(
    os.path.dirname(__file__), 'models'
)

# =========================
# FastAPI
# =========================

app = FastAPI(
    title=CONFIG['system']['name'],
    description=CONFIG['system']['description'],
    version=CONFIG['system']['version']
)
app.include_router(analytics.router)
app.include_router(model.router)
app.include_router(templates.router)

# -------------------------

app.mount(
    '/static',
    StaticFiles(
        directory=os.path.join(os.path.dirname(__file__),
        'static'
    )), name='static'
)

# =========================
# Cache
# =========================

@lru_cache(maxsize=1)
def load_dataset(data_path: str) -> pd.DataFrame:
    return pd.read_parquet(
        os.path.join(data_path, 'udse.parquet'),
        engine='fastparquet'
    )

# =========================
# Events
# =========================

@app.on_event('startup')
def set_paths():
    app.state.CONFIG = CONFIG
    app.state.DATA_PATH = DATA_PATH
    app.state.MODELS_PATH = MODELS_PATH
    app.state.DF = load_dataset(app.state.DATA_PATH)

@app.on_event('startup')
def load_model():
    active_model = model_api.load_active_model(app.state.MODELS_PATH)
    app.state.model = active_model['model_joblib']
    app.state.model_html = active_model['model_html']
    app.state.model_metadata = active_model['model_metadata']

@app.on_event('startup')
def init_registry():
    app.state.model_registry = model_api.load_registry(MODELS_PATH)

@app.middleware('http')
async def add_config_to_request(request: Request, call_next):
    request.state.config = CONFIG
    response = await call_next(request)
    return response

async def handle_exception(request: Request, exc: Exception):
    return error_page(request, exc)

app.add_exception_handler(Exception, handle_exception)
app.add_exception_handler(HTTPException, handle_exception)
app.add_exception_handler(StarletteHTTPException, handle_exception)
