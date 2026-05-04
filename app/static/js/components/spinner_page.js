/////////////////////////
/**
 * Spinner Page :: Components
 */
/////////////////////////

document.addEventListener('DOMContentLoaded', () => {
    const min_delay = new Promise(resolve => setTimeout(resolve, 1000));
    const page_load = new Promise(resolve => window.addEventListener('load', resolve));

    Promise.all([min_delay, page_load]).then(() => {
        document.querySelector('#spinner-page').remove();
    });
});

/////////////////////////
