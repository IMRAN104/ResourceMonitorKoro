from flask import Blueprint, render_template, jsonify
import psutil
import time

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@bp.route('/api/resource_metrics')
def resource_metrics():
    # Collect resource metrics
    cpu_usage = psutil.cpu_percent(interval=1)  # Wait for 1 second to get accurate CPU usage
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_usage = psutil.disk_usage('/').percent

    metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'top_processes': get_top_processes()
    }

    print(metrics)  # Debug log to verify data
    return jsonify(metrics)

def get_top_processes():
    # Call psutil.process_iter twice to ensure accurate CPU usage data
    psutil.cpu_percent(interval=None)  # Initialize CPU usage stats
    time.sleep(1)  # Wait for 1 second to collect CPU usage data

    # Collect processes with their CPU usage
    processes = [
        (p.info['name'], p.info['cpu_percent'])
        for p in psutil.process_iter(['name', 'cpu_percent'])
        if p.info['cpu_percent'] > 0  # Filter out processes with 0% CPU usage
    ]
    processes.sort(key=lambda x: x[1], reverse=True)  # Sort by CPU usage in descending order
    return processes[:5]  # Return the top 5 processes