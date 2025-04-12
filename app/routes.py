# app/routes.py
from flask import Blueprint, render_template, jsonify, current_app
import psutil
import time
import logging

bp = Blueprint('main', __name__)

@bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@bp.route('/api/resource_metrics')
def resource_metrics():
    try:
        # Get CPU, memory, and disk usage
        cpu_usage = psutil.cpu_percent(interval=0.1)  # Small interval for better responsiveness
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        disk_usage = psutil.disk_usage('/').percent
        
        # Get top processes (with error handling)
        try:
            top_processes = get_top_processes(5)
        except Exception as e:
            logging.error(f"Error getting processes: {str(e)}")
            top_processes = []
        
        # Create response
        response = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'top_processes': top_processes,
            'processes_closed': []  # No processes closed in this example
        }
        
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in resource_metrics: {str(e)}")
        return jsonify({
            'error': str(e),
            'cpu_usage': 0,
            'memory_usage': 0, 
            'disk_usage': 0,
            'top_processes': [],
            'processes_closed': []
        }), 500

def get_top_processes(limit=5):
    """Get the top resource-hungry processes"""
    processes = []
    
    # First call to initialize CPU tracking
    for _ in psutil.process_iter(['pid', 'name']):
        pass
    
    # Wait briefly to get meaningful CPU data
    time.sleep(0.1)
    
    # Second call to get actual data
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            # Get basic process info
            pid = proc.info['pid']
            name = proc.info['name']
            cpu_percent = proc.info['cpu_percent']
            
            # Get memory info (might fail for some processes)
            try:
                memory_info = proc.memory_info()
                # Calculate memory percent based on total system memory
                total_memory = psutil.virtual_memory().total
                memory_percent = (memory_info.rss / total_memory) * 100
            except:
                memory_percent = 0
            
            # Only include processes using CPU
            if cpu_percent > 0:
                processes.append({
                    'pid': pid,
                    'name': name,
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes that can't be accessed
            continue
    
    # Sort processes by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    # Return top N processes
    return processes[:limit]