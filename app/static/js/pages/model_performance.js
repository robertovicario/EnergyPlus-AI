/////////////////////////
/**
 * Model Performance :: Pages
 */
/////////////////////////

function apply_plotly_theme() {

    // Theming
    const is_light = document.documentElement.getAttribute('data-bs-theme') === 'light';
    const theme = is_light ? {
        axisColor: '#252525',
        fontColor: '#252525',
        gridColor: '#f5f5f5'
    } : {
        axisColor: '#f5f5f5',
        fontColor: '#f5f5f5',
        gridColor: '#252525'
    };

    // -------------------------

    // Plot EUI Distribution
    const relayout_eui_dist = {
        autosize: true,
        font: { color: theme.fontColor },
        xaxis: {
            gridcolor: theme.gridColor,
            zerolinecolor: theme.gridColor,
            linecolor: theme.axisColor
        },
        yaxis: {
            gridcolor: theme.gridColor,
            zerolinecolor: theme.gridColor,
            linecolor: theme.axisColor
        }
    };
    const plot_eui_dist = document.getElementById('plot-eui-dist');
    Plotly.relayout(plot_eui_dist, relayout_eui_dist);

    // Correlations
    const relayout_heatmap = {
        autosize: true,
        font: { color: theme.fontColor }
    };
    const plot_heatmap = document.getElementById('plot-heatmap');
    Plotly.relayout(plot_heatmap, relayout_heatmap);
}

window.addEventListener('load', () => {
    setTimeout(apply_plotly_theme, 100);
});
document.addEventListener('DOMContentLoaded', () => {
    new MutationObserver(apply_plotly_theme).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-bs-theme']
    });
});

/////////////////////////
