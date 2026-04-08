/**
 * AI Detector & Humanizer - Frontend Application
 */

const API_BASE = 'http://127.0.0.1:8000/api';

// ==================== DOM ELEMENTS ====================
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// Tabs
const tabBtns = $$('.tab-btn');
const tabContents = $$('.tab-content');

// Detection
const detectText = $('#detect-text');
const charCount = $('#char-count');
const analyzeBtn = $('#analyze-btn');
const resultsSection = $('#results-section');
const toggleBtns = $$('.toggle-btn');
const textInputArea = $('#text-input-area');
const fileInputArea = $('#file-input-area');
const dropzone = $('#dropzone');
const fileUpload = $('#file-upload');
const fileInfo = $('#file-info');
const fileName = $('#file-name');
const clearFileBtn = $('#clear-file');

// Results
const scoreRing = $('#score-ring');
const ringFill = $('#ring-fill');
const scoreNumber = $('#score-number');
const verdictText = $('#verdict-text');
const verdictMessage = $('#verdict-message');
const textStats = $('#text-stats');
const detailBars = $('#detail-bars');
const flaggedSection = $('#flagged-section');
const flaggedPhrases = $('#flagged-phrases');
const humanizeFromResult = $('#humanize-from-result');

// Humanizer
const humanizeText = $('#humanize-text');
const humanizeBtn = $('#humanize-btn');
const intensityBtns = $$('.intensity-btn');
const humanizeResults = $('#humanize-results');
const originalText = $('#original-text');
const humanizedText = $('#humanized-text');
const changesList = $('#changes-list');
const copyBtn = $('#copy-btn');
const recheckBtn = $('#recheck-btn');

// History
const histTabs = $$('.hist-tab');
const historyList = $('#history-list');

// Toast
const toast = $('#toast');

// State
let selectedFile = null;
let currentInputMode = 'text';
let currentIntensity = 'medium';
let lastDetectedText = '';
let lastHumanizedText = '';

// ==================== TAB NAVIGATION ====================
function switchTab(tab) {
    tabBtns.forEach(b => b.classList.remove('active'));
    tabContents.forEach(tc => {
        tc.classList.remove('active');
        tc.classList.add('hidden');
    });
    // Find and activate the matching tab button
    tabBtns.forEach(b => { if (b.dataset.tab === tab) b.classList.add('active'); });
    const target = $(`#tab-${tab}`);
    target.classList.remove('hidden');
    target.classList.add('active');

    if (tab === 'history') loadHistory();
}

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});

// ==================== INPUT TOGGLE ====================
toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = btn.dataset.input;
        currentInputMode = mode;
        toggleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        textInputArea.classList.toggle('hidden', mode !== 'text');
        fileInputArea.classList.toggle('hidden', mode !== 'file');
    });
});

// ==================== CHARACTER COUNT ====================
detectText.addEventListener('input', () => {
    charCount.textContent = detectText.value.length;
});

// ==================== FILE UPLOAD ====================
dropzone.addEventListener('click', () => fileUpload.click());

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

fileUpload.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

clearFileBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInfo.classList.add('hidden');
    fileUpload.value = '';
});

function handleFileSelect(file) {
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.classList.remove('hidden');
}

// ==================== ANALYZE ====================
analyzeBtn.addEventListener('click', async () => {
    if (currentInputMode === 'text') {
        const text = detectText.value.trim();
        if (text.length < 50) {
            showToast('Please enter at least 50 characters.', 'error');
            return;
        }
        await analyzeText(text);
    } else {
        if (!selectedFile) {
            showToast('Please select a file to upload.', 'error');
            return;
        }
        await analyzeFile(selectedFile);
    }
});

async function analyzeText(text) {
    setLoading(analyzeBtn, true);
    lastDetectedText = text;

    try {
        const res = await fetch(`${API_BASE}/detection/analyze/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });
        const data = await res.json();

        if (res.ok) {
            displayResults(data);
        } else {
            showToast(data.error || 'Analysis failed.', 'error');
        }
    } catch (err) {
        showToast('Could not connect to the server. Make sure the backend is running.', 'error');
    } finally {
        setLoading(analyzeBtn, false);
    }
}

async function analyzeFile(file) {
    setLoading(analyzeBtn, true);

    try {
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch(`${API_BASE}/detection/upload/`, {
            method: 'POST',
            body: formData,
        });
        const data = await res.json();

        if (res.ok) {
            // Store the detected text from the textarea if available, or use a placeholder
            lastDetectedText = detectText.value.trim() || '[File content analyzed]';
            displayResults(data);
        } else {
            showToast(data.error || 'File analysis failed.', 'error');
        }
    } catch (err) {
        showToast('Could not connect to the server. Make sure the backend is running.', 'error');
    } finally {
        setLoading(analyzeBtn, false);
    }
}

// ==================== DISPLAY RESULTS ====================
function displayResults(data) {
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    const score = data.ai_probability;

    // Score ring animation
    const circumference = 2 * Math.PI * 52; // r=52
    const offset = circumference - (score / 100) * circumference;

    scoreRing.className = 'score-ring';
    if (score >= 65) scoreRing.classList.add('score-high');
    else if (score >= 35) scoreRing.classList.add('score-medium');
    else scoreRing.classList.add('score-low');

    setTimeout(() => {
        ringFill.style.strokeDashoffset = offset;
    }, 100);

    // Animate score number
    animateNumber(scoreNumber, 0, score, 1200);

    // Verdict
    const verdicts = {
        'ai_generated': 'AI Generated',
        'likely_ai': 'Likely AI',
        'mixed': 'Mixed Content',
        'likely_human': 'Likely Human',
        'human': 'Human Written',
    };
    verdictText.textContent = verdicts[data.verdict] || data.verdict;
    verdictMessage.textContent = data.message;

    // Stats
    if (data.stats) {
        textStats.innerHTML = `
            <span class="stat-item"><strong>${data.stats.word_count}</strong> words</span>
            <span class="stat-item"><strong>${data.stats.sentence_count}</strong> sentences</span>
            <span class="stat-item"><strong>${data.stats.character_count}</strong> characters</span>
        `;
    }

    // Detail bars
    if (data.details) {
        const labels = {
            'perplexity': 'Perplexity',
            'burstiness': 'Burstiness',
            'vocabulary': 'Vocabulary',
            'phrase_detection': 'AI Phrases',
            'structure': 'Structure',
            'repetition': 'Repetition',
            'readability_uniformity': 'Readability',
        };

        detailBars.innerHTML = '';
        for (const [key, val] of Object.entries(data.details)) {
            const weight = data.weights ? data.weights[key] : '';
            const barColor = val >= 65 ? 'var(--danger)' : val >= 35 ? 'var(--warning)' : 'var(--secondary)';

            const row = document.createElement('div');
            row.className = 'detail-row';
            row.innerHTML = `
                <span class="detail-label">${labels[key] || key} ${weight ? `(${weight}%)` : ''}</span>
                <div class="detail-bar">
                    <div class="detail-bar-fill" style="background: ${barColor};"></div>
                </div>
                <span class="detail-score">${val}%</span>
            `;
            detailBars.appendChild(row);

            // Animate bar
            setTimeout(() => {
                row.querySelector('.detail-bar-fill').style.width = `${val}%`;
            }, 200);
        }
    }

    // Flagged phrases
    if (data.flagged_phrases && data.flagged_phrases.length > 0) {
        flaggedSection.classList.remove('hidden');
        flaggedPhrases.innerHTML = data.flagged_phrases
            .map(p => `<span class="phrase-tag">"${escapeHtml(p)}"</span>`)
            .join('');
    } else {
        flaggedSection.classList.add('hidden');
    }
}

// ==================== HUMANIZE ====================
humanizeBtn.addEventListener('click', async () => {
    const text = humanizeText.value.trim();
    if (text.length < 20) {
        showToast('Please enter at least 20 characters.', 'error');
        return;
    }

    setLoading(humanizeBtn, true);

    try {
        const res = await fetch(`${API_BASE}/humanizer/humanize/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, intensity: currentIntensity }),
        });
        const data = await res.json();

        if (res.ok) {
            displayHumanizeResults(text, data);
        } else {
            showToast(data.error || 'Humanization failed.', 'error');
        }
    } catch (err) {
        showToast('Could not connect to the server. Make sure the backend is running.', 'error');
    } finally {
        setLoading(humanizeBtn, false);
    }
});

intensityBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        intensityBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentIntensity = btn.dataset.intensity;
    });
});

function displayHumanizeResults(original, data) {
    humanizeResults.classList.remove('hidden');
    humanizeResults.scrollIntoView({ behavior: 'smooth', block: 'start' });

    originalText.textContent = original;
    humanizedText.textContent = data.humanized_text;
    lastHumanizedText = data.humanized_text;

    changesList.innerHTML = '';
    if (data.changes_made && data.changes_made.length > 0) {
        data.changes_made.forEach(change => {
            const li = document.createElement('li');
            li.textContent = change;
            changesList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No significant changes needed.';
        changesList.appendChild(li);
    }
}

// Copy humanized text
copyBtn.addEventListener('click', () => {
    if (lastHumanizedText) {
        navigator.clipboard.writeText(lastHumanizedText).then(() => {
            showToast('Copied to clipboard!', 'success');
        }).catch(() => {
            showToast('Failed to copy.', 'error');
        });
    }
});

// Recheck humanized text
recheckBtn.addEventListener('click', () => {
    if (lastHumanizedText) {
        switchTab('detect');

        // Fill in the text
        detectText.value = lastHumanizedText;
        charCount.textContent = lastHumanizedText.length;

        // Make sure text input mode is active
        toggleBtns.forEach(b => b.classList.remove('active'));
        toggleBtns[0].classList.add('active');
        textInputArea.classList.remove('hidden');
        fileInputArea.classList.add('hidden');
        currentInputMode = 'text';

        // Auto-analyze
        setTimeout(() => analyzeText(lastHumanizedText), 300);
    }
});

// Humanize from detection results
humanizeFromResult.addEventListener('click', () => {
    // Use lastDetectedText, or fall back to whatever is in the detect textarea
    const textToHumanize = lastDetectedText || detectText.value.trim();
    if (textToHumanize && textToHumanize !== '[File content analyzed]') {
        switchTab('humanize');

        humanizeText.value = textToHumanize;

        // Auto-trigger humanization after a short delay to ensure DOM is ready
        setTimeout(() => {
            const text = humanizeText.value.trim();
            if (text.length >= 20) {
                humanizeBtn.click();
            }
        }, 300);
    } else {
        showToast('No text available to humanize. Please paste text first.', 'error');
    }
});

// ==================== HISTORY ====================
let currentHistType = 'detections';

histTabs.forEach(btn => {
    btn.addEventListener('click', () => {
        histTabs.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentHistType = btn.dataset.hist;
        loadHistory();
    });
});

async function loadHistory() {
    const endpoint = currentHistType === 'detections'
        ? `${API_BASE}/detection/history/`
        : `${API_BASE}/humanizer/history/`;

    try {
        const res = await fetch(endpoint);
        const data = await res.json();

        if (data.results && data.results.length > 0) {
            historyList.innerHTML = data.results.map(item => {
                if (currentHistType === 'detections') {
                    const score = item.ai_probability;
                    const badgeClass = score >= 65 ? 'badge-high' : score >= 35 ? 'badge-medium' : 'badge-low';
                    return `
                        <div class="history-item">
                            <span class="history-preview">${escapeHtml(item.preview)}</span>
                            <div class="history-meta">
                                <span class="history-badge ${badgeClass}">${score}% AI</span>
                                <span class="history-date">${formatDate(item.created_at)}</span>
                            </div>
                        </div>
                    `;
                } else {
                    return `
                        <div class="history-item">
                            <span class="history-preview">${escapeHtml(item.original_preview)}</span>
                            <div class="history-meta">
                                <span class="history-badge badge-medium">${item.intensity}</span>
                                <span class="history-date">${formatDate(item.created_at)}</span>
                            </div>
                        </div>
                    `;
                }
            }).join('');
        } else {
            historyList.innerHTML = '<p class="empty-state">No history yet. Start by analyzing some text!</p>';
        }
    } catch (err) {
        historyList.innerHTML = '<p class="empty-state">Could not load history. Make sure the backend is running.</p>';
    }
}

// ==================== UTILITIES ====================
function setLoading(btn, loading) {
    const text = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.btn-loading');
    if (loading) {
        text.classList.add('hidden');
        loader.classList.remove('hidden');
        btn.disabled = true;
    } else {
        text.classList.remove('hidden');
        loader.classList.add('hidden');
        btn.disabled = false;
    }
}

function animateNumber(el, start, end, duration) {
    const startTime = performance.now();
    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.round(start + (end - start) * eased * 10) / 10;
        el.textContent = current.toFixed(1);
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    setTimeout(() => toast.classList.add('hidden'), 3500);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function formatDate(isoStr) {
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}
