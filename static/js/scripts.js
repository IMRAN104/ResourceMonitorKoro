// This file contains JavaScript code for dynamic updates on the frontend dashboard, such as fetching resource metrics at regular intervals.

const fetchResourceMetrics = async () => {
    try {
        const response = await fetch('/api/resource_metrics');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error fetching resource metrics:', error);
        document.getElementById('cpu-value').innerText = 'Error';
        document.getElementById('memory-value').innerText = 'Error';
        document.getElementById('disk-value').innerText = 'Error';
    }
};

const updateDashboard = (data) => {
    // Update resource metrics display
    document.getElementById('cpu-value').innerText = `${data.cpu_usage}%`;
    document.getElementById('memory-value').innerText = `${data.memory_usage}%`;
    document.getElementById('disk-value').innerText = `${data.disk_usage}%`;

    // Update top 5 resource-hungry processes
    const processList = document.getElementById('process-list');
    processList.innerHTML = '';
    data.top_processes.forEach(process => {
        const listItem = document.createElement('li');
        listItem.innerText = `${process[0]} - ${process[1]}% CPU`;
        processList.appendChild(listItem);
    });
    // Show alert if resource usage exceeds 90%
    const alertMessage = document.getElementById('alert-message');
    if (data.cpu_usage >= 90 || data.memory_usage >= 90) {
        alertMessage.style.display = 'block';
    } else {
        alertMessage.style.display = 'none';
    }
};

// Fetch resource metrics every minute
setInterval(fetchResourceMetrics, 1*1000);
fetchResourceMetrics(); // Initial fetch on load