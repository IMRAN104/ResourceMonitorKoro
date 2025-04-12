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
    # Get CPU, memory, and disk usage
    cpu_usage = psutil.cpu_percent(interval=0.5)  # Small interval for better responsiveness
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    disk_usage = psutil.disk_usage('/').percent
    
    # Get top processes
    top_processes = get_top_processes(5)
    
    # Check if resources exceed threshold and take action
    threshold = current_app.config.get('RESOURCE_THRESHOLD', 90)
    predefined_processes = current_app.config.get('PREDEFINED_PROCESSES_TO_CLOSE', [])
    
    # Initialize processes_closed list
    processes_closed = []
    
    # Check if we need to close processes due to high resource usage
    if memory_usage >= threshold or cpu_usage >= threshold:
        logging.warning(f"Resource threshold exceeded: CPU {cpu_usage}%, Memory {memory_usage}%")
        
        # Close predefined processes if configured
        if predefined_processes:
            processes_closed = close_predefined_processes(predefined_processes)
            
            # Log the action
            if processes_closed:
                logging.info(f"Closed processes due to high resource usage: {', '.join(processes_closed)}")
    
    response = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'top_processes': top_processes,
        'processes_closed': processes_closed,
        'threshold_exceeded': memory_usage >= threshold or cpu_usage >= threshold
    }
    
    return jsonify(response)

def get_top_processes(limit=5):
    """Get the top resource-hungry processes"""
    # Get all processes
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            # Get process info
            process_info = proc.info
            
            # Only include processes actually using resources
            processes.append({
                'pid': process_info['pid'],
                'name': process_info['name'],
                'cpu_percent': process_info['cpu_percent'],
                'memory_percent': process_info.get('memory_percent', 0)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes that can't be accessed
            pass
    
    # Sort by CPU usage (higher first)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    # Return top N processes
    return processes[:limit]

def close_predefined_processes(predefined_processes):
    """Close the predefined processes if they are running"""
    closed_processes = []
    
    for process_name in predefined_processes:
        logging.info(f"Looking for process to close: {process_name}")
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Check if this is a process we want to close
                if proc.info['name'].lower() == process_name.lower():
                    # Try to terminate the process
                    proc_pid = proc.info['pid']
                    proc_name = proc.info['name']
                    
                    logging.info(f"Attempting to terminate process: {proc_name} (PID: {proc_pid})")
                    
                    try:
                        # First try graceful termination
                        proc.terminate()
                        
                        # Wait briefly to see if it terminates
                        gone, still_alive = psutil.wait_procs([proc], timeout=3)
                        
                        # If still running, force kill
                        if still_alive:
                            logging.warning(f"Process {proc_name} didn't terminate gracefully, force killing")
                            proc.kill()
                        
                        closed_processes.append(proc_name)
                        logging.info(f"Successfully closed process: {proc_name}")
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                        logging.error(f"Failed to close process {proc_name}: {str(e)}")
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Skip if we can't access the process info
                continue
    
    return closed_processes