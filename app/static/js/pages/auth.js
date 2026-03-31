/////////////////////////
/**
 * Authentication :: Pages
 */
/////////////////////////

document.addEventListener('DOMContentLoaded', () => {
    localStorage.clear();

    // -------------------------

    const form_login = document.getElementById('form-login');
    const btn_login = document.getElementById('btn-login');

    btn_login.addEventListener('click', () => {
        if (form_login.checkValidity()) {
            show_spinner(btn_login, 'Logging in...');
            form_login.requestSubmit();
        } else {
            form_login.reportValidity();
        }
    });
});

/////////////////////////
