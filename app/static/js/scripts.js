// app/static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    updateLastUpdated();
    fetchResourceMetrics();
    
    // Set up periodic refresh
    setInterval(fetchResourceMetrics, 5000); // Refresh every 5 seconds
    setInterval(updateLastUpdated, 60000); // Update the "last updated" text every minute
});

function updateLastUpdated() {
    const lastUpdatedElement = document.getElementById('last-updated');
    if (lastUpdatedElement) {
        const now = new Date();
        lastUpdatedElement.textContent = now.toLocaleTimeString();
    }
}

async function fetchResourceMetrics() {
    try {
        console.log("Fetching resource metrics...");
        const response = await fetch('/api/resource_metrics');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Received data:", data);
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching resource metrics:', error);
        showError();
    }
}

function updateDashboard(data) {
    // Update gauges
    updateGauge('cpu', data.cpu_usage);
    updateGauge('memory', data.memory_usage);
    updateGauge('disk', data.disk_usage);
    
    // Update process list
    updateProcessList(data.top_processes);
    
    // Show/hide alert
    updateAlert(data);
    
    // Show/hide actions taken
    if (data.processes_closed) {
        updateActions(data.processes_closed);
    }
}

function updateGauge(type, value) {
    const gaugeElement = document.getElementById(`${type}-gauge`);
    const valueElement = document.getElementById(`${type}-value`);
    
    if (!gaugeElement || !valueElement) {
        console.warn(`Gauge elements for ${type} not found`);
        return;
    }
    
    // Update the gauge fill
    gaugeElement.style.width = `${value}%`;
    
    // Update the gauge color based on value
    if (value >= 90) {
        gaugeElement.style.backgroundColor = 'var(--danger-color)';
    } else if (value >= 70) {
        gaugeElement.style.backgroundColor = 'var(--warning-color)';
    } else {
        gaugeElement.style.backgroundColor = 'var(--success-color)';
    }
    
    // Update the value text
    valueElement.textContent = `${value.toFixed(1)}%`;
}

function updateProcessList(processes) {
    const processList = document.getElementById('process-list');
    if (!processList) {
        console.warn('Process list element not found');
        return;
    }
    
    processList.innerHTML = '';
    console.log("Updating process list with:", processes);
    
    if (!processes || processes.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="4" class="loading-text">No processes found</td>';
        processList.appendChild(row);
        return;
    }
    
    processes.forEach(process => {
        const row = document.createElement('tr');
        
        // Handle different possible data structures
        const pid = process.pid || (Array.isArray(process) ? process[0] : 'N/A');
        const name = process.name || (Array.isArray(process) && process[1] && process[1].name ? process[1].name : 'Unknown');
        const cpuPercent = process.cpu_percent || (Array.isArray(process) && process[1] && process[1].cpu_percent ? process[1].cpu_percent : 0);
        const memoryPercent = process.memory_percent || (Array.isArray(process) && process[1] && process[1].memory_percent ? process[1].memory_percent : 0);
        
        row.innerHTML = `
            <td>${pid}</td>
            <td>${name}</td>
            <td>${typeof cpuPercent === 'number' ? cpuPercent.toFixed(1) : cpuPercent}%</td>
            <td>${typeof memoryPercent === 'number' ? memoryPercent.toFixed(1) : memoryPercent}%</td>
        `;
        
        processList.appendChild(row);
    });
}

function updateAlert(data) {
    const alertContainer = document.getElementById('alert-container');
    const alertDetails = document.getElementById('alert-details');
    
    if (!alertContainer || !alertDetails) {
        console.warn('Alert elements not found');
        return;
    }
    
    if (data.cpu_usage >= 90 || data.memory_usage >= 90 || data.disk_usage >= 90) {
        // Show alert
        alertContainer.classList.remove('hidden');
        
        // Build alert details
        let detailsHTML = '<ul>';
        if (data.cpu_usage >= 90) {
            detailsHTML += `<li>CPU usage is at ${data.cpu_usage.toFixed(1)}%</li>`;
        }
        if (data.memory_usage >= 90) {
            detailsHTML += `<li>Memory usage is at ${data.memory_usage.toFixed(1)}%</li>`;
        }
        if (data.disk_usage >= 90) {
            detailsHTML += `<li>Disk usage is at ${data.disk_usage.toFixed(1)}%</li>`;
        }
        detailsHTML += '</ul>';
        
        alertDetails.innerHTML = detailsHTML;
    } else {
        // Hide alert
        alertContainer.classList.add('hidden');
    }
}

function updateActions(closedProcesses) {
    const actionsContainer = document.getElementById('actions-container');
    const actionsList = document.getElementById('actions-list');
    
    if (!actionsContainer || !actionsList) {
        console.warn('Actions elements not found');
        return;
    }
    
    if (closedProcesses && closedProcesses.length > 0) {
        // Show actions
        actionsContainer.classList.remove('hidden');
        
        // Build actions list
        actionsList.innerHTML = '';
        closedProcesses.forEach(process => {
            const li = document.createElement('li');
            li.textContent = process;
            actionsList.appendChild(li);
        });
    } else {
        // Hide actions
        actionsContainer.classList.add('hidden');
    }
}

function showError() {
    // Update CPU value
    const cpuValue = document.getElementById('cpu-value');
    if (cpuValue) cpuValue.textContent = 'Error';
    
    // Update memory value
    const memoryValue = document.getElementById('memory-value');
    if (memoryValue) memoryValue.textContent = 'Error';
    
    // Update disk value
    const diskValue = document.getElementById('disk-value');
    if (diskValue) diskValue.textContent = 'Error';
    
    // Update process list with error message
    const processList = document.getElementById('process-list');
    if (processList) {
        processList.innerHTML = '<tr><td colspan="4" class="loading-text">Error fetching data</td></tr>';
    }
}