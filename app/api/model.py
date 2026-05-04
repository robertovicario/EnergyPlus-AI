# =========================
# Dependencies
# =========================

from datetime import datetime
from fastapi import Request
from scipy.stats import gaussian_kde
import joblib
import json
import numpy as np
import os
import plotly.graph_objects as go
import yaml

# =========================
# APIs
# =========================

def load_active_model(MODELS_PATH: str):

    # Pointer
    pointer_path = os.path.join(
        MODELS_PATH, 'registry', 'pointer.yaml'
    )
    with open(pointer_path) as r:
        pointer = yaml.safe_load(r)

    # Model
    active_version = pointer.get('version')
    model_path = os.path.join(
        MODELS_PATH, 'registry', active_version
    )

    # Model Joblib
    model_joblib = joblib.load(
        os.path.join(model_path, 'model.joblib')
    )

    # Model HTML
    with open(os.path.join(model_path, 'model.html')) as f:
        model_html = f.read()

    # Model Metadata
    with open(os.path.join(model_path, 'metadata.json')) as f:
        model_metadata = json.load(f)

    # -------------------------

    return {
        'model_joblib': model_joblib,
        'model_html': model_html,
        'model_metadata': model_metadata
    }

def load_registry(MODELS_PATH: str):

    # Helper fxs
    def parse_timestamp(date_string: str) -> datetime:
        return datetime.strptime(date_string, "%d %B %Y, %H:%M:%S")

    # -------------------------

    # Pointer
    with open(os.path.join(MODELS_PATH, 'registry', 'pointer.yaml')) as r:
        pointer = yaml.safe_load(r)
    active_version = pointer.get('version')

    # Registry
    registry = {}
    registry_path = os.path.join(MODELS_PATH, 'registry')

    for version in os.listdir(registry_path):
        version_path = os.path.join(registry_path, version)
        if not os.path.isdir(version_path):
            continue

        metadata_path = os.path.join(version_path, 'metadata.json')
        if not os.path.exists(metadata_path):
            continue

        with open(metadata_path) as f:
            metadata = json.load(f)

        model_id = metadata.get('id', version)
        registry[version] = {
            'id': model_id,
            'timestamp': metadata.get('timestamp'),
            'stage': 'active' if version == active_version else 'archived',
            'metadata': metadata,
            'config': metadata.get('config')
        }

    # Experiments
    exp_path = os.path.join(MODELS_PATH, 'experiments')
    for exp_dir in os.listdir(exp_path):
        exp_dir_path = os.path.join(exp_path, exp_dir)
        if not os.path.isdir(exp_dir_path):
            continue

        metadata_path = os.path.join(exp_dir_path, 'metadata.json')
        if not os.path.exists(metadata_path):
            continue

        with open(metadata_path) as f:
            metadata = json.load(f)

        model_id = metadata.get('id', exp_dir)
        registry[model_id] = {
            'id': model_id,
            'timestamp': metadata.get('timestamp'),
            'stage': 'experiment',
            'metadata': metadata,
            'config': metadata.get('config')
        }

    # Stage
    stage_order = {
        'active': 0,
        'experiment': 1,
        'archived': 2
    }
    registry = dict(sorted(
        registry.items(),
        key=lambda x: (
            stage_order[x[1]['stage']],
            -parse_timestamp(x[1]['metadata']['timestamp']).timestamp()
        )
    ))

    # -------------------------

    return registry

def get_badges(model_metadata) -> dict:

    # Descriptive
    std = model_metadata['metrics']['descriptive']['std']
    q1 = model_metadata['metrics']['descriptive']['q1']
    q3 = model_metadata['metrics']['descriptive']['q3']

    # MAE
    mae = model_metadata['metrics']['regression']['test']['mae']
    mae_ratio = mae / max(q3 - q1, 1e-9)

    if mae_ratio <= 0.2:
        mae_b = 'Low'
    elif mae_ratio <= 0.5:
        mae_b = 'Moderate'
    else:
        mae_b = 'High'

    # RMSE
    rmse = model_metadata['metrics']['regression']['test']['rmse']
    rmse_ratio = rmse / max(std, 1e-9)

    if rmse_ratio <= 0.5:
        rmse_b = 'Stable'
    elif rmse_ratio <= 1.0:
        rmse_b = 'Acceptable'
    else:
        rmse_b = 'Unstable'

    # R2
    r2 = model_metadata['metrics']['regression']['test']['r2']
    r2_percent = r2 * 100

    if r2_percent >= 90:
        r2_b = 'Excellent'
    elif r2_percent >= 70:
        r2_b = 'Good'
    else:
        r2_b = 'Weak'

    # -------------------------

    return {
        'mae': {
            'keyword': mae_b,
            'value': f"{mae_ratio:.2f}",
            'theme': 'success' if mae_b == 'Low' else 'body' if mae_b == 'Moderate' else 'danger'
        },
        'rmse': {
            'keyword': rmse_b,
            'value': f"{rmse_ratio:.2f}",
            'theme': 'success' if rmse_b == 'Stable' else 'body' if rmse_b == 'Acceptable' else 'danger'
        },
        'r2': {
            'keyword': r2_b,
            'value': f"{r2_percent:.2f}%",
            'theme': 'success' if r2_b == 'Excellent' else 'body' if r2_b == 'Good' else 'danger'
        }
    }

def get_plot_eui_dist(request: Request) -> str:

    # Dataset
    df = request.app.state.DF
    FRAC = 0.2
    subset = int(len(df) * FRAC)
    df = df.sample(n=subset, random_state=42)
    target = df['EUI']

    # -------------------------

    # Histogram
    hist = go.Histogram(
        histnorm='probability density',
        marker=dict(
            color='#1f77b4',
            line=dict(color='white', width=1)
        ),
        name='Distribution',
        nbinsx=50,
        x=target
    )

    # KDE
    kde = gaussian_kde(target)
    x = np.linspace(target.min(), target.max(), 200)
    y = kde(x)
    line = go.Scatter(
        fill='tozeroy',
        fillcolor='rgba(255,127,14,0.4)',
        line=dict(color='#ff7f0e', width=2),
        mode='lines',
        name='Density',
        x=x,
        y=y
    )

    # -------------------------

    # Figure
    fig = go.Figure([hist, line])
    fig.update_layout(
        font=dict(color='#252525'),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            x=1,
            xanchor='right',
            y=1,
            yanchor='top'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor='#f5f5f5',
            linecolor='#252525',
            title='EUI',
            zerolinecolor='rgba(0,0,0,0.08)'
        ),
        yaxis=dict(
            gridcolor='#f5f5f5',
            linecolor='#252525',
            title='Density',
            zerolinecolor='rgba(0,0,0,0.08)'
        )
    )

    # -------------------------

    return fig.to_html(
        div_id='plot-eui-dist',
        config={ 'responsive': True, 'displayModeBar': False },
        full_html=False,
        include_plotlyjs='cdn'
    )

def get_plot_heatmap(request: Request) -> str:

    # Dataset
    df = request.app.state.DF
    FRAC = 0.2
    subset = int(len(df) * FRAC)
    df = df.sample(n=subset, random_state=42)
    df_num = df.select_dtypes(include=[np.number]).iloc[:subset]

    # -------------------------

    # Correlation
    corr = df_num.corr()
    order = corr['EUI'].abs().sort_values(ascending=False).index
    corr = corr.loc[order, order]

    # Heatmap
    heatmap = go.Heatmap(
        colorscale='RdBu_r',
        hovertemplate="x: %{x}<br>y: %{y}<br>corr: %{z:.2f}<extra></extra>",
        x=corr.columns,
        y=corr.columns,
        z=corr,
        zmin=-1,
        zmax=1
    )

    # -------------------------

    # Figure
    fig = go.Figure(data=[heatmap])
    fig.update_layout(
        font=dict(color='#252525'),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(autorange='reversed')
    )

    # -------------------------

    return fig.to_html(
        div_id='plot-heatmap',
        config={ 'responsive': True, 'displayModeBar': False },
        full_html=False,
        include_plotlyjs='cdn'
    )
