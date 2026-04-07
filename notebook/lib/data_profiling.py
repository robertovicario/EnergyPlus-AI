# =========================
# Dependencies
# =========================

from ydata_profiling import ProfileReport
import os
import pandas as pd
import webbrowser

# =========================
# Methods
# =========================

def profile_data(
    df: pd.DataFrame,
    path: str='.trash/',
    title: str='YData Profiling Report'
) -> None:
    """
    Profiles the given DataFrame and generates an HTML report.

    Parameters:
        - `df` (`pd.DataFrame`): The DataFrame to profile.
        - `path` (`str`): The path where the output HTML file will be saved. Default is '.trash/'.
        - `title` (`str`): The title of the report. Default is 'YData Profiling Report'.
    """

    RES_PATH = os.path.abspath(path)
    if not os.path.exists(RES_PATH):
        os.makedirs(RES_PATH)

    out_file = os.path.join(RES_PATH, f"{title.replace(' ', '_')}.html")
    profiler = ProfileReport(df, explorative=True, title=title)
    profiler.to_file(out_file)

    # -------------------------

    webbrowser.open(f"file://{out_file}")

    # -------------------------

    return None
