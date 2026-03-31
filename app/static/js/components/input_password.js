/////////////////////////
/**
 * Input Password :: Components
 */
/////////////////////////

function togglePasswordView(input_id, button_id) {
    const eye_fill = `<i class="bi bi-eye-fill fs-5"></i>`;
    const eye_slash_fill = `<i class="bi bi-eye-slash-fill fs-5"></i>`;
    const input_password = document.getElementById(input_id);
    const btn_password_view = document.getElementById(button_id);

    if (input_password.type === 'password') {
        input_password.type = 'text';
        btn_password_view.innerHTML = eye_slash_fill;
    } else {
        input_password.type = 'password';
        btn_password_view.innerHTML = eye_fill;
    }
}

document.getElementById('btn-password-view')?.addEventListener('click', () => {
    togglePasswordView('input-password', 'btn-password-view');
});

const newPasswordButton = document.getElementById('btn-new-password-view');
if (newPasswordButton) {
    newPasswordButton.addEventListener('click', () => {
        togglePasswordView('input-new-password', 'btn-new-password-view');
    });
}

/////////////////////////
