# =========================
# Dependencies
# =========================

from fastapi import Request
from loguru import logger

# =========================
# Configurations
# =========================

logger.add('logs/app.log', rotation='5 MB')
logger.add('logs/db.log', rotation='5 MB')

# =========================
# Methods
# =========================

def log_request(request: Request):
    request_metadata = f"[{request.method}] {request.url.path}"
    logger.info(f"{'=' * len(request_metadata)}")
    logger.info(request_metadata)
    logger.info(f"{'-' * len(request_metadata)}")
