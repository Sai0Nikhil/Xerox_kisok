// Bittu Xerox Kiosk Interactive OS
let currentSessionId = null;
let currentOrder = null;
let countdownInterval = null;
let socket = null;
let scanCopies = 1;

// Web Audio API Sound Effects
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(freq, type, duration) {
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch(e) {}
}

function playBeep() { playTone(880, 'sine', 0.1); }
function playSuccessChime() {
    playTone(523.25, 'triangle', 0.2);
    setTimeout(() => playTone(659.25, 'triangle', 0.2), 120);
    setTimeout(() => playTone(783.99, 'triangle', 0.4), 240);
}
function playPrintSound() {
    playTone(180, 'sawtooth', 0.6);
}

// Initialize WebSockets
function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/kiosk`;
    
    socket = new WebSocket(wsUrl);
    
    socket.onopen = () => {
        console.log("Kiosk connected to WebSocket Server.");
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("WS Event received:", data);
        
        if (data.type === "FILE_UPLOADED") {
            playBeep();
            closeModals();
            displayOrderReview(data.order);
        } else if (data.type === "PAYMENT_SUCCESS") {
            startPrintingSequence(data.order);
        } else if (data.type === "STATUS_REFRESH") {
            if (data.paper_count !== undefined) {
                document.getElementById('paperTrayBadge').innerText = `${data.paper_count} / 500`;
            }
            if (data.toner_level !== undefined) {
                document.getElementById('tonerBadge').innerText = `${data.toner_level}%`;
            }
        }
    };
    
    socket.onclose = () => {
        setTimeout(initWebSocket, 2000);
    };
}

// Modal Handlers
function openMobileUploadModal() {
    playBeep();
    fetch('/api/session/new')
        .then(res => res.json())
        .then(data => {
            currentSessionId = data.session_id;
            const mobileUrl = `${window.location.origin}/mobile?session_id=${currentSessionId}`;
            
            const qrContainer = document.getElementById('kioskSessionQrContainer');
            qrContainer.innerHTML = '';
            new QRCode(qrContainer, {
                text: mobileUrl,
                width: 180,
                height: 180,
                colorDark: "#081c15",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });
            
            document.getElementById('mobileWebUrl').innerText = mobileUrl;
            document.getElementById('mobileDirectLink').href = `/mobile?session_id=${currentSessionId}`;
            document.getElementById('mobileQrModal').classList.remove('hidden');
        });
}

function openScannerModal() {
    playBeep();
    scanCopies = 1;
    document.getElementById('scanCopiesCount').innerText = scanCopies;
    document.getElementById('scannerModal').classList.remove('hidden');
}

function adjScanCopies(delta) {
    playBeep();
    scanCopies = Math.max(1, Math.min(20, scanCopies + delta));
    document.getElementById('scanCopiesCount').innerText = scanCopies;
}

function triggerScanAndReview() {
    playBeep();
    closeModals();
    const sessionId = 'SCN-' + Math.floor(1000 + Math.random() * 9000);
    const orderData = {
        session_id: sessionId,
        filename: 'Canon_Flatbed_Scanned_Doc.pdf',
        pages: 1,
        copies: scanCopies,
        total_amount: (scanCopies * 2.50).toFixed(2),
        preview_title: 'Instant Photocopy / Xerox'
    };
    displayOrderReview(orderData);
}

function openWhatsAppModal() {
    playBeep();
    document.getElementById('waPinInput').value = '';
    document.getElementById('whatsappModal').classList.remove('hidden');
}

function appendPin(num) {
    playBeep();
    const input = document.getElementById('waPinInput');
    if (input.value.length < 4) {
        input.value += num;
    }
}
function clearPin() {
    playBeep();
    document.getElementById('waPinInput').value = '';
}
function quickPin(pin) {
    document.getElementById('waPinInput').value = pin;
    submitPin();
}
function submitPin() {
    playBeep();
    const pin = document.getElementById('waPinInput').value;
    if (pin.length !== 4) return alert("Please enter a 4-digit PIN.");
    
    const formData = new FormData();
    formData.append('pin', pin);
    
    fetch('/api/whatsapp/verify-pin', {
        method: 'POST',
        body: formData
    })
    .then(res => {
        if (!res.ok) throw new Error("PIN not found");
        return res.json();
    })
    .then(data => {
        closeModals();
        displayOrderReview(data.order);
    })
    .catch(err => {
        alert("Invalid or expired WhatsApp PIN! Try demo PIN 7842.");
    });
}

function openErpModal() {
    playBeep();
    document.getElementById('erpModal').classList.remove('hidden');
}

function fetchErpDoc(type) {
    playBeep();
    const rollNo = document.getElementById('erpRollInput').value || '2100030142';
    const formData = new FormData();
    formData.append('roll_no', rollNo);
    formData.append('doc_type', type);
    
    fetch('/api/erp/fetch', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        closeModals();
        displayOrderReview(data.order);
    });
}

function closeModals() {
    document.getElementById('mobileQrModal').classList.add('hidden');
    document.getElementById('whatsappModal').classList.add('hidden');
    document.getElementById('erpModal').classList.add('hidden');
    document.getElementById('scannerModal').classList.add('hidden');
}

// Display Order Review and Dynamic UPI QR
function displayOrderReview(order) {
    currentOrder = order;
    document.getElementById('serviceSelectorView').classList.add('hidden');
    document.getElementById('orderReviewModal').classList.remove('hidden');
    
    document.getElementById('sessionTag').innerText = order.session_id;
    document.getElementById('orderFileName').innerText = order.filename;
    document.getElementById('orderPages').innerText = `${order.pages * (order.copies || 1)} Pages (${order.copies || 1} Copies)`;
    document.getElementById('orderTotalPayable').innerText = `₹${parseFloat(order.total_amount).toFixed(2)}`;
    
    // Render UPI QR
    const upiContainer = document.getElementById('upiQrCodeContainer');
    upiContainer.innerHTML = '';
    const upiUrl = order.qr_payload || `upi://pay?pa=paytmqr28100505@paytm&pn=BittuXerox&am=${order.total_amount}&cu=INR&tn=Kiosk-${order.session_id}`;
    
    new QRCode(upiContainer, {
        text: upiUrl,
        width: 170,
        height: 170,
        colorDark: "#081c15",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.M
    });
    
    // Start countdown
    let timeLeft = 120;
    clearInterval(countdownInterval);
    countdownInterval = setInterval(() => {
        timeLeft--;
        document.getElementById('countdownTimer').innerText = `${timeLeft}s`;
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            resetToHome();
        }
    }, 1000);
}

// Simulate Payment Approval
function simulatePaymentApproval() {
    playBeep();
    const formData = new FormData();
    formData.append('session_id', currentOrder ? currentOrder.session_id : 'DEMO-123');
    
    fetch('/api/pay/simulate', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log("Payment approved:", data);
    });
}

// Execution Sequence: Printing -> Shredding Memory -> Success
function startPrintingSequence(order) {
    clearInterval(countdownInterval);
    document.getElementById('orderReviewModal').classList.add('hidden');
    document.getElementById('printingAnimationView').classList.remove('hidden');
    
    let progress = 10;
    const pBar = document.getElementById('printingProgressBar');
    const pStatus = document.getElementById('printStatusSubtitle');
    
    const interval = setInterval(() => {
        progress += 20;
        pBar.style.width = `${progress}%`;
        playPrintSound();
        
        if (progress === 50) {
            pStatus.innerText = "Brother HL-L2321D Duplex Engine: Page 1-2 Outputting...";
        } else if (progress === 90) {
            pStatus.innerText = "FastAPI Zero-Storage: Executing RAM Shredder...";
        } else if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                document.getElementById('printingAnimationView').classList.add('hidden');
                document.getElementById('jobCompleteView').classList.remove('hidden');
                playSuccessChime();
                
                // Complete job on server
                const fData = new FormData();
                fData.append('session_id', order.session_id);
                fetch('/api/print/complete', { method: 'POST', body: fData });
            }, 600);
        }
    }, 800);
}

function resetToHome() {
    playBeep();
    clearInterval(countdownInterval);
    closeModals();
    document.getElementById('orderReviewModal').classList.add('hidden');
    document.getElementById('printingAnimationView').classList.add('hidden');
    document.getElementById('jobCompleteView').classList.add('hidden');
    document.getElementById('serviceSelectorView').classList.remove('hidden');
    currentOrder = null;
}

window.onload = () => {
    initWebSocket();
};
