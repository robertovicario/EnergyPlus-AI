/////////////////////////
/**
 * Model Overview :: Pages
 */
/////////////////////////

function sync_sklearn_theme() {
    const el = document.querySelector('#sk-container-id-3');
    el.classList.remove('light', 'dark');
    el.classList.add(
        document.documentElement.getAttribute('data-bs-theme')
    );
}

function sync_after_change() {
    setTimeout(sync_sklearn_theme, 0);
}

window.addEventListener('DOMContentLoaded', () => {
    sync_sklearn_theme();
    ['option1', 'option2'].forEach(id => {
        document.getElementById(id).addEventListener('change', sync_after_change);
    });
});

/////////////////////////
