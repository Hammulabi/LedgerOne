const THEME_KEY = 'ledgerone-theme';
const DEFAULT_THEME = 'dark';

function getStoredTheme() {
    const storedTheme = localStorage.getItem(THEME_KEY);
    return storedTheme === 'light' || storedTheme === 'dark' ? storedTheme : DEFAULT_THEME;
}

function setToggleLabel(theme) {
    const label = document.getElementById('theme-toggle-label');
    if (label) {
        label.textContent = theme === 'dark' ? '🌙' : '☀️';
    }

    const button = document.getElementById('theme-toggle');
    if (button) {
        button.setAttribute('aria-label', theme === 'dark' ? 'Activer le thème clair' : 'Activer le thème sombre');
        button.setAttribute('title', theme === 'dark' ? 'Activer le thème clair' : 'Activer le thème sombre');
    }
}

function applyTheme(theme, persist = true) {
    const safeTheme = theme === 'light' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', safeTheme);

    if (persist) {
        localStorage.setItem(THEME_KEY, safeTheme);
    }

    setToggleLabel(safeTheme);
}

function initTheme() {
    applyTheme(getStoredTheme(), false);

    const button = document.getElementById('theme-toggle');
    if (!button) {
        return;
    }

    button.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || DEFAULT_THEME;
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
    });
}

document.addEventListener('DOMContentLoaded', initTheme);
