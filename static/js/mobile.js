// Bittu Xerox Mobile Companion Script
let selectedFile = null;
let selectedPresetName = 'OS_Lab_Evaluation.pdf';
let pageCount = 6;
let copies = 1;
let colorMode = 'bw';
let duplex = true;
let sessionId = new URLSearchParams(window.location.search).get('session_id') || 'DEV-SESSION';

function initMobile() {
    document.getElementById('sessionTagDisplay').innerText = sessionId;
    calculatePrice();
    connectMobileWs();
}

function connectMobileWs() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/mobile/${sessionId}`);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'PAYMENT_CONFIRMED') {
            document.getElementById('sendToKioskBtn').innerText = "✅ Paid & Printing!";
            document.getElementById('sendToKioskBtn').classList.add('bg-emerald-700');
        }
    };
}

function handleFileSelected(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile = file;
        selectedPresetName = null;
        pageCount = Math.floor(Math.random() * 6) + 2; // Demo estimated pages
        
        document.getElementById('dropzoneBox').classList.add('hidden');
        document.getElementById('fileInfoBox').classList.remove('hidden');
        document.getElementById('selectedFileName').innerText = file.name;
        document.getElementById('selectedFileSize').innerText = `${(file.size / 1024 / 1024).toFixed(1)} MB • ~${pageCount} Pages`;
        calculatePrice();
    }
}

function clearSelectedFile() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfoBox').classList.add('hidden');
    document.getElementById('dropzoneBox').classList.remove('hidden');
    selectPreset('OS_Lab_Evaluation.pdf', 6);
}

function selectPreset(name, pages) {
    selectedPresetName = name;
    pageCount = pages;
    calculatePrice();
}

function changeCopies(delta) {
    copies = Math.max(1, Math.min(10, copies + delta));
    document.getElementById('copiesDisplay').innerText = copies;
    calculatePrice();
}

function setColorMode(mode) {
    colorMode = mode;
    if (mode === 'bw') {
        document.getElementById('modeBwBtn').className = 'px-3 py-1 rounded-lg bg-emerald-600 text-white';
        document.getElementById('modeColorBtn').className = 'px-3 py-1 rounded-lg text-slate-400';
    } else {
        document.getElementById('modeBwBtn').className = 'px-3 py-1 rounded-lg text-slate-400';
        document.getElementById('modeColorBtn').className = 'px-3 py-1 rounded-lg bg-cyan-600 text-white';
    }
    calculatePrice();
}

function calculatePrice() {
    const rate = colorMode === 'bw' ? 2.50 : 10.00;
    const total = (pageCount * copies * rate).toFixed(2);
    document.getElementById('mobileTotalPrice').innerText = `₹${total}`;
}

function submitToKiosk() {
    const btn = document.getElementById('sendToKioskBtn');
    btn.disabled = true;
    btn.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> Sending...`;

    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('copies', copies);
    formData.append('duplex', document.getElementById('duplexToggle').checked);
    formData.append('color_mode', colorMode);
    
    if (selectedFile) {
        formData.append('file', selectedFile);
    } else {
        formData.append('mock_filename', selectedPresetName);
        formData.append('mock_pages', pageCount);
    }

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        btn.innerHTML = `<i class="fa-solid fa-check"></i> Sent to Kiosk!`;
        btn.classList.replace('from-emerald-600', 'from-teal-600');
        document.getElementById('syncSuccessBanner').classList.remove('hidden');
    })
    .catch(err => {
        btn.disabled = false;
        btn.innerText = "Try Again";
        alert("Upload error. Please check server.");
    });
}

window.onload = initMobile;
