const DEFAULT_API_ORIGIN = ['8080', '5500'].includes(window.location.port)
    ? `${window.location.protocol}//${window.location.hostname}:8000`
    : window.location.origin;

const API_BASE_URL = window.__LEDGERONE_API_BASE_URL || `${DEFAULT_API_ORIGIN}/api`;
