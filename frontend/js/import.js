const uploadZone = document.getElementById('upload-zone');
const fileInput = document.getElementById('file-input');
const importButton = document.getElementById('import-button');
const selectedFileDiv = document.getElementById('selected-file');
const resultDiv = document.getElementById('result');
const previewBody = document.getElementById('preview-body');
const previewCard = document.getElementById('preview-card');

let selectedFile = null;

uploadZone.addEventListener('click', () => fileInput.click());
uploadZone.addEventListener('dragover', (e) => { e.preventDefault(); uploadZone.classList.add('dragover'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', (e) => { if (e.target.files.length > 0) handleFile(e.target.files[0]); });

async function handleFile(file) {
    if (!file.name.endsWith('.csv')) return showToast('Veuillez sélectionner un fichier CSV (.csv).');
    selectedFile = file;
    document.getElementById('file-name').textContent = sanitizeText(file.name);
    document.getElementById('file-size').textContent = formatFileSize(file.size);
    selectedFileDiv.style.display = 'flex';
    importButton.disabled = false;
    resultDiv.style.display = 'none';

    try {
        const preview = await previewCSV(file);
        renderPreview(preview);
    } catch (error) {
        showToast(error.message);
    }
}

function renderPreview(preview) {
    previewCard.style.display = 'block';
    previewBody.innerHTML = '';
    preview.preview_rows.forEach((row) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${sanitizeText(row.date)}</td><td>${sanitizeText(row.description)}</td><td>${sanitizeText(row.amount)}</td><td>${sanitizeText(row.category || '-')}</td>`;
        previewBody.appendChild(tr);
    });
    document.getElementById('detected-delimiter').textContent = preview.detected_delimiter;
    if (preview.errors?.length) showToast(preview.errors.join(' | '), 'warning');
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' o';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' Ko';
    return (bytes / (1024 * 1024)).toFixed(1) + ' Mo';
}

importButton.addEventListener('click', async () => {
    if (!selectedFile) return;
    importButton.disabled = true;
    try {
        const result = await importCSV(selectedFile);
        resultDiv.className = 'result-card result-success';
        resultDiv.innerHTML = `<strong>Import terminé</strong><p>${result.inserted} importées, ${result.skipped} ignorées.</p>`;
        resultDiv.style.display = 'block';
        if (result.errors?.length) showToast(result.errors.join(' | '), 'warning');
    } catch (error) {
        resultDiv.className = 'result-card result-error';
        resultDiv.innerHTML = `<strong>Échec de l'import</strong><p>${sanitizeText(error.message)}</p>`;
        resultDiv.style.display = 'block';
    } finally {
        importButton.disabled = false;
    }
});
