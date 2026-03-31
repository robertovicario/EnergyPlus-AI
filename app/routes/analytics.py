# =========================
# Dependencies
# =========================

from eppy.modeleditor import IDF
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from ladybug.epw import EPW
import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import tempfile
import zipfile

from config.logging import logger

# =========================
# Inference
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
IDD_FILE = os.path.join(DATA_PATH, 'config', 'Energy+.idd')
IDF_FILE = os.path.join(DATA_PATH, 'idf', 'AdultEducationCenter.idf')
EPW_FILE = os.path.join(DATA_PATH, 'epw', 'USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw')

# =========================
# IDF Configuration
# =========================

# IDF.setiddname(IDD_FILE)
# idf = IDF(IDF_FILE, EPW_FILE)

# building_name = idf.idfobjects['BUILDING'][0].Name
# num_zones = len(idf.idfobjects['ZONE'])
# num_spaces = len(idf.idfobjects['SPACE'])
# walls = [
#     s for s in idf.idfobjects['BUILDINGSURFACE:DETAILED']
#     if s.Surface_Type.upper() == 'WALL'
# ]
# num_walls = len(walls)
# windows = list(idf.idfobjects['WINDOW']) + list(idf.idfobjects['FENESTRATIONSURFACE:DETAILED'])
# num_windows = len(windows)
# doors = list(idf.idfobjects['DOOR']) + list(idf.idfobjects['GLAZEDDOOR'])
# num_doors = len(doors)

# floor_area = 0
# surfaces = idf.idfobjects['BUILDINGSURFACE:DETAILED']

# for s in surfaces:
#     area = s.area
#     if s.Surface_Type.upper() == 'FLOOR':
#         floor_area += area
# floor_area = int(round(floor_area, 0))

# dashboard = {
#     'Building-Name': building_name,
#     'EUI': 0,
#     'Floor-Area-M2': floor_area,
#     'Zones-Num': num_zones,
#     'Walls-Num': num_walls,
#     'Windows-Num': num_windows,
#     'Doors-Num': num_doors,
# }
# dashboard

router = APIRouter(prefix='/analytics', tags=['analytics'])

@router.post('/upload', name='analytics:upload')
async def upload(file: UploadFile = File(...)):
    try:
        # crea cartella temporanea
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, file.filename)

            # salva zip
            with open(zip_path, "wb") as f:
                f.write(await file.read())

            # estrai zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            # trova IDF e EPW
            idf_path, epw_path = None, None

            for root, _, files in os.walk(tmpdir):
                for f in files:
                    if f.endswith(".idf"):
                        idf_path = os.path.join(root, f)
                    elif f.endswith(".epw"):
                        epw_path = os.path.join(root, f)

            if not idf_path or not epw_path:
                return JSONResponse(
                    status_code=400,
                    content={"error": "IDF o EPW non trovati nello ZIP"}
                )

            # carica IDF
            IDF.setiddname(IDD_FILE)
            idf = IDF(idf_path, epw_path)

            # === ANALISI ===
            building_name = idf.idfobjects['BUILDING'][0].Name
            num_zones = len(idf.idfobjects['ZONE'])

            walls = [
                s for s in idf.idfobjects['BUILDINGSURFACE:DETAILED']
                if s.Surface_Type.upper() == 'WALL'
            ]
            num_walls = len(walls)

            windows = list(idf.idfobjects['WINDOW']) + list(idf.idfobjects['FENESTRATIONSURFACE:DETAILED'])
            num_windows = len(windows)

            doors = list(idf.idfobjects['DOOR']) + list(idf.idfobjects['GLAZEDDOOR'])
            num_doors = len(doors)

            floor_area = 0
            for s in idf.idfobjects['BUILDINGSURFACE:DETAILED']:
                if s.Surface_Type.upper() == 'FLOOR':
                    floor_area += s.area

            floor_area = int(round(floor_area, 0))

            dashboard = {
                'Building-Name': building_name,
                'Floor-Area-M2': floor_area,
                'Zones-Num': num_zones,
                'Walls-Num': num_walls,
                'Windows-Num': num_windows,
                'Doors-Num': num_doors,
            }

            fig = go.Figure()

            # -----------------------
            # funzione vertici
            # -----------------------
            def get_vertices(surface):
                n = int(surface.Number_of_Vertices)
                verts = []

                for i in range(n):
                    x = float(surface[f"Vertex_{i+1}_Xcoordinate"])
                    y = float(surface[f"Vertex_{i+1}_Ycoordinate"])
                    z = float(surface[f"Vertex_{i+1}_Zcoordinate"])
                    verts.append((x,y,z))

                return np.array(verts)


            # -----------------------
            # superficie piena
            # -----------------------
            def add_surface(surface, color, opacity=0.8):
                verts = get_vertices(surface)
                n = len(verts)

                i_idx = []
                j_idx = []
                k_idx = []

                for t in range(1, n-1):
                    i_idx.append(0)
                    j_idx.append(t)
                    k_idx.append(t+1)

                fig.add_trace(go.Mesh3d(
                    x=verts[:,0],
                    y=verts[:,1],
                    z=verts[:,2],
                    i=i_idx,
                    j=j_idx,
                    k=k_idx,
                    color=color,
                    opacity=opacity,
                    flatshading=True,
                    hovertext=surface.Name,
                    hoverinfo="text"
                ))


            # -----------------------
            # bordi superfici
            # -----------------------
            def add_edges(surface, color="red", width=4):
                verts = get_vertices(surface)

                xs = list(verts[:,0]) + [verts[0,0]]
                ys = list(verts[:,1]) + [verts[0,1]]
                zs = list(verts[:,2]) + [verts[0,2]]

                fig.add_trace(go.Scatter3d(
                    x=xs,
                    y=ys,
                    z=zs,
                    mode="lines",
                    line=dict(color=color, width=width),
                    hoverinfo="skip"
                ))


            # -----------------------
            # dati IDF
            # -----------------------
            surfaces = idf.idfobjects["BUILDINGSURFACE:DETAILED"]
            windows = idf.idfobjects["FENESTRATIONSURFACE:DETAILED"]

            # muri + pavimenti
            for s in surfaces:

                if s.Surface_Type == "Wall":
                    add_surface(s, "white", 1)
                    add_edges(s, "darkgray", 3)

                elif s.Surface_Type == "Floor":
                    add_surface(s, 'red', 0.3)
                    add_edges(s, "red", 6)

            # finestre + porte
            for w in windows:

                if w.Surface_Type == "Window":
                    add_surface(w, "skyblue", 1)
                    add_edges(w, "blue", 3)

                elif w.Surface_Type in ["Door", "GlassDoor"]:
                    add_surface(w, "brown", 1)
                    add_edges(w, "black", 4)


            # -----------------------
            # layout
            # -----------------------
            fig.update_layout(
                showlegend=False,
                scene=dict(
                    aspectmode="data",
                    xaxis=dict(visible=False, backgroundcolor='rgba(0, 0, 0, 0)'),
                    yaxis=dict(visible=False, backgroundcolor='rgba(0, 0, 0, 0)'),
                    zaxis=dict(visible=False, backgroundcolor='rgba(0, 0, 0, 0)'),
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.8))
                ),
                margin=dict(l=0, r=0, b=0, t=0),
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)'
            )
            rendering = fig.to_json()

            return {
                "widgets": dashboard,
                "rendering": rendering
            }

    except Exception as e:
        logger.error(str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
