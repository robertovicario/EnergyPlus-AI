# =========================
# Dependencies
# =========================

from ydata_profiling import ProfileReport
import os
import webbrowser

# =========================
# Methods
# =========================

def profile_data(
    df,
    file_name='data_profiling',
    report_title='YData Profiling Report'
):
    """
    Profiles the given DataFrame and generates an HTML report.

    Parameters:
        - `df` (`pd.DataFrame`): The DataFrame to profile.
        - `file_name` (`str`): The name of the output HTML file. Default is 'data_profiling'.
        - `report_title` (`str`): The title of the report. Default is 'YData Profiling Report'.
    """

    RES_PATH = os.path.abspath('../res/data-profiling')
    if not os.path.exists(RES_PATH):
        os.makedirs(RES_PATH)

    OUT_FILE = os.path.join(RES_PATH, f"{file_name}.html")
    profile = ProfileReport(df, explorative=True, title=report_title)
    profile.to_file(OUT_FILE)

    # -------------------------

    webbrowser.open(f"file://{OUT_FILE}")
