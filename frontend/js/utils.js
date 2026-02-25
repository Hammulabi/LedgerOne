function sanitizeText(value) {
    const text = value == null ? '' : String(value);
    return text.replace(/[<>"'`]/g, '');
}

function showToast(message, type = 'error') {
    const container = document.body;
    const el = document.createElement('div');
    el.className = `user-message ${type}`;
    el.textContent = sanitizeText(message);
    container.appendChild(el);
    setTimeout(() => el.remove(), 5000);
}

function setGlobalLoading(isLoading) {
    let overlay = document.getElementById('global-loading-overlay');
    if (isLoading) {
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'global-loading-overlay';
            overlay.className = 'global-loading';
            overlay.innerHTML = '<div class="spinner"></div><p>Chargement...</p>';
            document.body.appendChild(overlay);
        }
    } else if (overlay) {
        overlay.remove();
    }
}
