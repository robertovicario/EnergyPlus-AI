# =========================
# Dependencies
# =========================

from datetime import datetime, timezone
import os

# =========================
# Configurations
# =========================

now = datetime.now(timezone.utc)

# -------------------------

dynamic = {
    'app': {
        'secret_key': os.getenv('APP_SECRET_KEY'),
        'host': os.getenv('APP_HOST'),
        'port': os.getenv('APP_PORT'),
        'debug': os.getenv('APP_DEBUG')
    },
    'time': {
        'timestamp': now.timestamp(),
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'isoformat': now.isoformat()
    }
}
