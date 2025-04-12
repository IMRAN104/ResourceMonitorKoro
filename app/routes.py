# app/routes.py
from flask import Blueprint, render_template, jsonify, current_app
from .utils import get_system_metrics, get_top_resource_hungry_processes, monitor_resources
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@bp.route('/api/resource_metrics')
def resource_metrics():
    # Get system metrics
    metrics = get_system_metrics()
    
    # Get top processes
    top_processes = get_top_resource_hungry_processes(5)
    
    # Check if we need to monitor and take action
    predefined_processes = current_app.config.get('PREDEFINED_PROCESSES_TO_CLOSE', [])
    threshold = current_app.config.get('RESOURCE_THRESHOLD', 90)
    alert_config = {
        'method': current_app.config.get('ALERT_METHOD', 'slack'),
        'slack_webhook_url': current_app.config.get('SLACK_WEBHOOK_URL', ''),
        'whatsapp_to': current_app.config.get('WHATSAPP_TO', ''),
        'whatsapp_from': current_app.config.get('WHATSAPP_FROM', ''),
        'whatsapp_token': current_app.config.get('WHATSAPP_TOKEN', '')
    }
    
    monitor_result = monitor_resources(threshold, predefined_processes, alert_config)
    
    # Format processes for JSON response
    formatted_processes = [
        {
            'pid': proc['pid'],
            'name': proc['name'],
            'cpu_percent': proc['cpu_percent'],
            'memory_percent': proc['memory_percent']
        }
        for proc in top_processes
    ]
    
    response = {
        'cpu_usage': metrics['cpu_usage'],
        'memory_usage': metrics['memory_usage'],
        'disk_usage': metrics['disk_usage'],
        'top_processes': formatted_processes,
        'alerts_sent': monitor_result['alerts_sent'],
        'processes_closed': monitor_result['processes_closed']
    }
    
    return jsonify(response)