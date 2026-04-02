# =========================
# Dependencies
# =========================

import os
import requests
import traceback

# =========================
# Configurations
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_API = 'https://api.github.com/repos/robertovicario/EnergyPlus-AI/contents'
IDD_URL = 'https://raw.githubusercontent.com/robertovicario/EnergyPlus-AI/main/app/data/config/Energy+.idd'
CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'data', 'config'))
TEMPLATES_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'templates'))
DOWNLOAD_MAP = {
    'app/data/config': CONFIG_PATH,
    'app/templates': TEMPLATES_PATH,
}

# =========================
# Methods
# =========================

def download_idd():
    os.makedirs(CONFIG_PATH, exist_ok=True)
    dest = os.path.join(CONFIG_PATH, "Energy+.idd")

    if os.path.exists(dest):
        print("IDD already exists")
        return

    r = requests.get(IDD_URL, timeout=10)
    r.raise_for_status()

    with open(dest, "wb") as f:
        f.write(r.content)

def download_templates(repo_path: str, local_path: str):
    try:
        os.makedirs(local_path, exist_ok=True)
        url = f"{BASE_API}/{repo_path}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        items = response.json()

        if not isinstance(items, list):
            raise RuntimeError()

        for item in items:
            if item['type'] == 'dir':
                download_templates(item['path'], os.path.join(local_path, item['name']))

            elif item['type'] == 'file':
                dest = os.path.join(local_path, item['name'])

                if os.path.exists(dest):
                    continue

                r = requests.get(item['download_url'], timeout=10)
                r.raise_for_status()

                with open(dest, 'wb') as f:
                    f.write(r.content)
    except Exception:
        traceback.print_exc()
        raise

def init():
    download_idd()
    download_templates('app/templates', TEMPLATES_PATH)

# =========================
# Entrypoint
# =========================

if __name__ == '__main__':
    init()
