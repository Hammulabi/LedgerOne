function getErrorMessage(errorData, status) {
    if (errorData?.error?.message) return errorData.error.message;
    if (typeof errorData?.detail === 'string') return errorData.detail;
    return `Erreur HTTP ${status}`;
}

async function apiRequest(path, options = {}, { showLoader = true } = {}) {
    try {
        if (showLoader && typeof setGlobalLoading === 'function') setGlobalLoading(true);
        const response = await fetch(`${API_BASE_URL}${path}`, options);
        const data = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error(getErrorMessage(data, response.status));
        return data;
    } catch (error) {
        if (error instanceof TypeError) {
            throw new Error('Impossible de contacter le serveur. Vérifiez votre connexion réseau.');
        }
        throw error;
    } finally {
        if (showLoader && typeof setGlobalLoading === 'function') setGlobalLoading(false);
    }
}

async function getAllCategories() { return apiRequest('/categories/'); }
async function getCategoryById(id) { return apiRequest(`/categories/${id}`); }
async function createCategory(categoryData) { return apiRequest('/categories/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(categoryData) }); }
async function updateCategory(id, categoryData) { return apiRequest(`/categories/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(categoryData) }); }
async function deleteCategory(id) { return apiRequest(`/categories/${id}`, { method: 'DELETE' }); }

async function getAllTransactions(params = {}) {
    const q = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== '') q.append(k, v); });
    return apiRequest(`/transactions/?${q.toString()}`);
}
async function searchTransactionsAdvanced(params = {}) {
    const q = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== null && v !== '') q.append(k, v); });
    return apiRequest(`/transactions/search-advanced?${q.toString()}`);
}
async function getTransactionById(id) { return apiRequest(`/transactions/${id}`); }
async function createTransaction(transactionData) { return apiRequest('/transactions/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(transactionData) }); }
async function updateTransaction(id, transactionData) { return apiRequest(`/transactions/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(transactionData) }); }
async function deleteTransaction(id) { return apiRequest(`/transactions/${id}`, { method: 'DELETE' }); }

async function getSettings() { return apiRequest('/settings/'); }
async function updateSettings(globalBudget) { return apiRequest('/settings/', { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ global_monthly_budget: globalBudget }) }); }

async function getMonthlySummary(year, month) { return apiRequest(`/insights/summary?year=${year}&month=${month}`); }
async function getMonthlyTotal(year, month, categoryId = null) { return apiRequest(`/insights/monthly-total?year=${year}&month=${month}${categoryId ? `&category_id=${categoryId}` : ''}`); }
async function getCategoryBreakdown(year, month) { return apiRequest(`/insights/category-breakdown?year=${year}&month=${month}`); }
async function getAnnualExpenses(year) { return apiRequest(`/insights/annual-expenses?year=${year}`); }
async function getMonthlyEvolution(year, month) { return apiRequest(`/insights/monthly-evolution?year=${year}&month=${month}`); }
async function getSavingsGoal(year, month, income, goal) { return apiRequest(`/insights/savings-goal?year=${year}&month=${month}&income=${income}&goal=${goal}`); }

async function getBudgetAlerts(year, month) { return apiRequest(`/alerts/?year=${year}&month=${month}`); }

async function previewCSV(file) {
    const formData = new FormData();
    formData.append('file', file);
    return apiRequest('/import/preview', { method: 'POST', body: formData });
}
async function importCSV(file) {
    const formData = new FormData();
    formData.append('file', file);
    return apiRequest('/import/csv', { method: 'POST', body: formData });
}
