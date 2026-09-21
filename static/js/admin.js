// Admin IoT Telemetry & Business Dashboard Script
let socket = null;
let trafficChart = null;

function initAdmin() {
    initTrafficChart();
    connectAdminWs();
}

function connectAdminWs() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/admin`;
    socket = new WebSocket(wsUrl);

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'TELEMETRY_UPDATE') {
            document.getElementById('adminTemp').innerText = `${data.temperature}°C`;
            document.getElementById('adminFanRpm').innerText = `${data.fan_rpm} RPM (Dual Fan)`;
            document.getElementById('adminPaperCount').innerText = data.paper_count;
            document.getElementById('adminPaperBar').style.width = `${(data.paper_count / 500) * 100}%`;
            document.getElementById('adminTonerLevel').innerText = `${data.toner_level}%`;
        } else if (data.type === 'NEW_TRANSACTION') {
            // Update financial cards
            document.getElementById('adminRevenueToday').innerText = `₹${parseFloat(data.revenue_today).toFixed(2)}`;
            document.getElementById('adminProfitToday').innerText = `₹${(data.revenue_today * 0.52).toFixed(2)}`;
            document.getElementById('adminPaperCount').innerText = data.paper_count;
            document.getElementById('adminPaperBar').style.width = `${(data.paper_count / 500) * 100}%`;
            
            // Add row to table
            const tbody = document.getElementById('transactionTableBody');
            const row = document.createElement('tr');
            row.className = 'hover:bg-slate-800/40 transition bg-emerald-950/20';
            row.innerHTML = `
                <td class="p-3 font-bold text-teal-300">${data.txn.id}</td>
                <td class="p-3 text-slate-400">${data.txn.time}</td>
                <td class="p-3 font-semibold">${data.txn.type}</td>
                <td class="p-3">${data.txn.pages} Sheets</td>
                <td class="p-3 font-bold text-brand-gold">₹${parseFloat(data.txn.amount).toFixed(2)}</td>
                <td class="p-3 text-slate-400">${data.txn.upi_ref}</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">${data.txn.status}</span></td>
            `;
            tbody.insertBefore(row, tbody.firstChild);
        }
    };

    socket.onclose = () => {
        setTimeout(connectAdminWs, 2000);
    };
}

function initTrafficChart() {
    const ctx = document.getElementById('trafficChart').getContext('2d');
    
    // Hourly distribution from 6 AM to 2 AM next day (Hostel profile)
    const hours = ['6 AM', '8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM', '10 PM', '11 PM', '12 AM', '1 AM', '2 AM'];
    const volumes = [15, 65, 45, 30, 20, 55, 75, 110, 140, 125, 90, 45, 20];
    
    trafficChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hours,
            datasets: [{
                label: 'Pages Printed / Hour',
                data: volumes,
                borderColor: '#5bc0be',
                backgroundColor: 'rgba(91, 192, 190, 0.15)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#ffd166',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 10 } }
                }
            }
        }
    });
}

function refillPaper() {
    fetch('/api/admin/refill-paper', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            document.getElementById('adminPaperCount').innerText = 500;
            document.getElementById('adminPaperBar').style.width = '100%';
            alert("Paper Tray Refilled to 500 Sheets (1 Ream).");
        });
}

function triggerAdminAction(action) {
    const formData = new FormData();
    formData.append('action', action);
    
    fetch('/api/admin/trigger-action', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (action === 'TOGGLE_DOOR') {
            const btn = document.getElementById('doorStatusBtn');
            if (data.door_locked) {
                btn.innerHTML = `<i class="fa-solid fa-lock mr-1"></i> LOCKED`;
                btn.className = 'px-3 py-1 bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 rounded-lg font-bold';
            } else {
                btn.innerHTML = `<i class="fa-solid fa-lock-open mr-1"></i> UNLOCKED`;
                btn.className = 'px-3 py-1 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded-lg font-bold';
            }
        } else {
            alert(`Admin action triggered: ${action}`);
        }
    });
}

window.onload = initAdmin;
