import psutil

def get_system_metrics():
    metrics = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
    }
    return metrics

def get_top_resource_hungry_processes(top_n=5):
    processes = [(p.pid, p.info) for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info'])]
    processes.sort(key=lambda x: x[1]['cpu_percent'], reverse=True)
    return processes[:top_n]

def send_alert(message, method='slack'):
    if method == 'slack':
        # Implement Slack alert logic here
        pass
    elif method == 'whatsapp':
        # Implement WhatsApp alert logic here
        pass

def close_predefined_processes(predefined_processes):
    for process_name in predefined_processes:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.terminate()  # or proc.kill() for forceful termination
                break

def monitor_resources(threshold=90, predefined_processes=None):
    metrics = get_system_metrics()
    if metrics['cpu_usage'] >= threshold:
        send_alert(f"Alert: CPU usage is at {metrics['cpu_usage']}%", method='slack')
        if predefined_processes:
            close_predefined_processes(predefined_processes)