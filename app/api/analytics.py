# =========================
# Dependencies
# =========================

from eppy.modeleditor import IDF
import numpy as np
import plotly.graph_objects as go

# =========================
# APIs
# =========================

def get_widgets(idf: IDF) -> dict:

    # Widgets (1)
    building_name = idf.idfobjects['BUILDING'][0].Name
    floor_area = 0
    for s in idf.idfobjects['BUILDINGSURFACE:DETAILED']:
        if s.Surface_Type.upper() == 'FLOOR':
            floor_area += s.area
    floor_area = int(round(floor_area, 0))

    # Widgets (2)
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

    # -------------------------

    return {
        'Building-Name': building_name,
        'Floor-Area-M2': floor_area,
        'Zones-Num': num_zones,
        'Walls-Num': num_walls,
        'Windows-Num': num_windows,
        'Doors-Num': num_doors,
    }

def get_rendering(idf: IDF) -> str:

    # Helper fxs
    def get_vertices(surface):
        n = int(surface.Number_of_Vertices)
        verts = []

        for i in range(n):
            x = float(surface[f"Vertex_{i+1}_Xcoordinate"])
            y = float(surface[f"Vertex_{i+1}_Ycoordinate"])
            z = float(surface[f"Vertex_{i+1}_Zcoordinate"])
            verts.append((x,y,z))

        return np.array(verts)

    def add_surface(fig, surface, color, opacity=0.8):
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
            hoverinfo='text'
        ))

    def add_edges(fig, surface, color='red', width=4):
        verts = get_vertices(surface)
        xs = list(verts[:,0]) + [verts[0,0]]
        ys = list(verts[:,1]) + [verts[0,1]]
        zs = list(verts[:,2]) + [verts[0,2]]

        fig.add_trace(go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode='lines',
            line=dict(color=color, width=width),
            hoverinfo='skip'
        ))

    # -------------------------

    # Rendering
    fig = go.Figure()
    surfaces = idf.idfobjects['BUILDINGSURFACE:DETAILED']
    windows = idf.idfobjects['FENESTRATIONSURFACE:DETAILED']

    for s in surfaces:
        if s.Surface_Type == 'Wall':
            add_surface(fig, s, 'white', 1)
            add_edges(fig, s, 'darkgray', 3)
        elif s.Surface_Type == 'Floor':
            add_surface(fig, s, 'red', 0.3)
            add_edges(fig, s, 'red', 6)

    for w in windows:
        if w.Surface_Type == 'Window':
            add_surface(fig, w, 'skyblue', 1)
            add_edges(fig, w, 'blue', 3)
        elif w.Surface_Type in ['Door', 'GlassDoor']:
            add_surface(fig, w, 'brown', 1)
            add_edges(fig, w, 'black', 4)

    fig.update_layout(
        showlegend=False,
        scene=dict(
            aspectmode='data',
            xaxis=dict(visible=False, backgroundcolor='rgba(0, 0, 0, 0)'),
            yaxis=dict(visible=False, backgroundcolor='rgba(0, 0, 0, 0)'),
            zaxis=dict(visible=False, backgroundcolor='rgba(0, 0, 0, 0)'),
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.8))
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )

    # -------------------------

    return fig.to_json()
