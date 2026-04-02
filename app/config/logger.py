# =========================
# Dependencies
# =========================

from fastapi import Request
from loguru import logger

# =========================
# Configurations
# =========================

logger.add('logs/app.log', rotation='5 MB')

# =========================
# Methods
# =========================

def log_request(request: Request):
    logger.info(f"{'=' * 50}")
    logger.info(f"[{request.method}] {request.url.path}")
    logger.info(f"{'-' * 50}")
