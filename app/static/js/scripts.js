// app/static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    updateLastUpdated();
    fetchResourceMetrics();
    
    // Set up periodic refresh
    setInterval(fetchResourceMetrics, 10000); // Refresh every 10 seconds
    setInterval(updateLastUpdated, 60000); // Update the "last updated" text every minute
});

function updateLastUpdated() {
    const now = new Date();
    document.getElementById('last-updated').textContent = now.toLocaleTimeString();
}

async function fetchResourceMetrics() {
    try {
        const response = await fetch('/api/resource_metrics');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
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
    updateActions(data.processes_closed);
    
    // Update last updated time
    updateLastUpdated();
}

function updateGauge(type, value) {
    const gaugeElement = document.getElementById(`${type}-gauge`);
    const valueElement = document.getElementById(`${type}-value`);
    
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
    processList.innerHTML = '';
    
    if (!processes || processes.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="4" class="loading-text">No process data available</td>';
        processList.appendChild(row);
        return;
    }
    
    processes.forEach(process => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${process.pid}</td>
            <td>${process.name}</td>
            <td>${process.cpu_percent.toFixed(1)}%</td>
            <td>${process.memory_percent.toFixed(1)}%</td>
        `;
        
        processList.appendChild(row);
    });
}

function updateAlert(data) {
    const alertContainer = document.getElementById('alert-container');
    const alertDetails = document.getElementById('alert-details');
    
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
    document.getElementById('cpu-value').textContent = 'Error';
    document.getElementById('memory-value').textContent = 'Error';
    document.getElementById('disk-value').textContent = 'Error';
    
    const processList = document.getElementById('process-list');
    processList.innerHTML = '<tr><td colspan="4" class="loading-text">Error fetching data</td></tr>';
}