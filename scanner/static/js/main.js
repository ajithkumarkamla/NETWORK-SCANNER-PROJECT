document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scan-btn');
    const ipInput = document.getElementById('ip-range');
    const deviceList = document.getElementById('device-list');
    const deviceCountElem = document.getElementById('device-count');
    const healthElem = document.getElementById('network-health');
    let isScanning = false;

    // 1. Initial Load: Fetch existing active devices
    fetchDevices();

    // 2. Immediate Auto-Discovery
    // Trigger scan as soon as the page is ready
    console.log("Auto-Discovery triggered on load...");
    triggerScan();

    // 3. Periodic UI Refresh (Every 30 seconds to check for new devices)
    setInterval(fetchDevices, 30000);

    scanBtn.addEventListener('click', () => {
        triggerScan();
    });

    async function triggerScan() {
        if (isScanning) return;

        const ipRange = ipInput.value || '192.168.1.0/24';
        isScanning = true;
        scanBtn.disabled = true;
        scanBtn.innerText = 'Scanning...';

        if (healthElem) healthElem.innerText = 'Discovery in Progress...';

        // Optionally clear table to "only show found devices" from THIS scan
        // deviceList.innerHTML = '<tr><td colspan="6" style="text-align:center;">Scanning network... Please wait.</td></tr>';

        try {
            const response = await fetch('/api/scan/start/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ip_range: ipRange })
            });
            const data = await response.json();

            if (data.status === 'success') {
                // Update list precisely with what was FOUND in this scan
                updateDeviceList(data.devices);
                console.log(`Scan complete! Found ${data.devices.length} devices.`);
                if (healthElem) healthElem.innerText = 'Optimal (Scan finished)';
            } else {
                console.error('Scan failed:', data.message);
                if (healthElem) healthElem.innerText = 'Scan Error (Check Npcap)';
                alert("Scan Error: " + data.message);
            }
        } catch (error) {
            console.error('Scan error:', error);
            if (healthElem) healthElem.innerText = 'Network Error';
        } finally {
            isScanning = false;
            scanBtn.disabled = false;
            scanBtn.innerText = 'Start Scan';
        }
    }

    async function fetchDevices() {
        try {
            const response = await fetch('/api/devices/');
            const data = await response.json();
            // In manual refresh, we show all known active devices
            updateDeviceList(data.devices);
        } catch (error) {
            console.error('Error fetching devices:', error);
        }
    }

    function updateDeviceList(devices) {
        deviceList.innerHTML = '';
        deviceCountElem.innerText = devices.length;

        if (devices.length === 0) {
            deviceList.innerHTML = '<tr><td colspan="6" style="text-align:center;">No active devices found.</td></tr>';
            return;
        }

        devices.forEach(device => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${device.ip}</td>
                <td>${device.mac || 'N/A'}</td>
                <td>${device.hostname || 'Unknown'}</td>
                <td><span class="status-badge ${device.is_active ? 'status-online' : 'status-offline'}">${device.is_active ? 'Online' : 'Offline'}</span></td>
                <td>${device.open_ports ? device.open_ports.join(', ') : 'None'}</td>
                <td><button onclick="viewHistory(${device.id})" class="btn-sm">History</button></td>
            `;
            deviceList.appendChild(row);
        });
    }
});

async function viewHistory(deviceId) {
    const modal = document.getElementById('history-modal');
    const details = document.getElementById('history-details');
    modal.style.display = 'block';

    try {
        const response = await fetch(`/api/history/${deviceId}/`);
        const data = await response.json();

        let html = '<table><thead><tr><th>Time</th><th>Ports</th><th>Status</th></tr></thead><tbody>';
        data.history.forEach(h => {
            html += `<tr><td>${h.time}</td><td>${h.ports.join(', ') || 'None'}</td><td>${h.status}</td></tr>`;
        });
        html += '</tbody></table>';
        details.innerHTML = html;
    } catch (error) {
        details.innerHTML = 'Error loading history.';
    }
}

document.querySelector('.close').onclick = () => {
    document.getElementById('history-modal').style.display = 'none';
}
window.onclick = (event) => {
    const modal = document.getElementById('history-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
