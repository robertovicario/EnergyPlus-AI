# =========================
# Dependencies
# =========================

from fastapi import Request
from functools import lru_cache
import os
import pandas as pd

# =========================
# APIs
# =========================

@lru_cache(maxsize=1)
def load_dataset(request: Request) -> pd.DataFrame:
    return pd.read_parquet(
        os.path.join(request.app.state.DATA_PATH, 'udse.parquet'),
        engine='fastparquet'
    )
