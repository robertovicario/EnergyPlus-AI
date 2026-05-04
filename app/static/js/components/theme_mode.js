/////////////////////////
/**
 * Theme Mode :: Components
 */
/////////////////////////

document.addEventListener('DOMContentLoaded', function() {
    const html = document.documentElement;
    const btn_light = document.querySelector('#option1');
    const btn_dark = document.querySelector('#option2');
    const saved_theme = localStorage.getItem('theme');

    // Saved Theme
    if (saved_theme) {
        const prefers_dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = prefers_dark ? 'dark' : 'light';
        html.setAttribute('data-bs-theme', theme);
        html.setAttribute('data-bs-theme', saved_theme);

        if (saved_theme === 'dark') {
            btn_dark.checked = true;
        } else {
            btn_light.checked = true;
        }
    }

    // Light Mode
    btn_light?.addEventListener('change', function() {
        if (this.checked) {
            html.setAttribute('data-bs-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });

    // Dark Mode
    btn_dark?.addEventListener('change', function() {
        if (this.checked) {
            html.setAttribute('data-bs-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        }
    });
});

/////////////////////////
