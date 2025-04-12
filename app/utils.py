# app/utils.py
import psutil
import requests
import time
import logging

def get_system_metrics():
    metrics = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
    }
    return metrics

def get_top_resource_hungry_processes(top_n=5):
    # First call to initialize CPU measurement
    processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
    
    # Wait briefly to get meaningful CPU data
    time.sleep(0.5)
    
    # Second call to get actual CPU usage
    processes = [
        {
            'pid': p.pid,
            'name': p.info['name'],
            'cpu_percent': p.info['cpu_percent'],
            'memory_percent': p.info['memory_percent'] if p.info['memory_percent'] else 0
        }
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
    ]
    
    # Sort by CPU usage (primary) and memory usage (secondary)
    processes.sort(key=lambda x: (x['cpu_percent'], x['memory_percent']), reverse=True)
    return processes[:top_n]

def send_slack_alert(message, webhook_url):
    try:
        payload = {'text': message}
        requests.post(webhook_url, json=payload)
        logging.info(f"Slack alert sent: {message}")
        return True
    except Exception as e:
        logging.error(f"Failed to send Slack alert: {str(e)}")
        return False

def send_whatsapp_alert(message, to_number, from_number, auth_token):
    # This is a placeholder for WhatsApp integration
    # You would typically use a service like Twilio for WhatsApp messaging
    logging.info(f"WhatsApp alert would be sent: {message}")
    return True

def send_alert(message, method='slack', config=None):
    if not config:
        config = {}
        
    if method == 'slack':
        webhook_url = config.get('slack_webhook_url', '')
        return send_slack_alert(message, webhook_url)
    elif method == 'whatsapp':
        to_number = config.get('whatsapp_to', '')
        from_number = config.get('whatsapp_from', '')
        auth_token = config.get('whatsapp_token', '')
        return send_whatsapp_alert(message, to_number, from_number, auth_token)
    else:
        logging.warning(f"Unknown alert method: {method}")
        return False

def close_predefined_processes(predefined_processes):
    closed_processes = []
    for process_name in predefined_processes:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                try:
                    proc.terminate()  # Try to terminate gracefully first
                    closed_processes.append(process_name)
                    logging.info(f"Terminated process: {process_name} (PID: {proc.pid})")
                except:
                    try:
                        proc.kill()  # Force kill if terminate doesn't work
                        closed_processes.append(process_name)
                        logging.info(f"Force killed process: {process_name} (PID: {proc.pid})")
                    except Exception as e:
                        logging.error(f"Failed to kill process {process_name}: {str(e)}")
    return closed_processes

def monitor_resources(threshold=90, predefined_processes=None, alert_config=None):
    metrics = get_system_metrics()
    alerts_sent = False
    processes_closed = []
    
    # Check if any metric exceeds threshold
    if any(metrics[key] >= threshold for key in ['cpu_usage', 'memory_usage', 'disk_usage']):
        # Create alert message
        alert_message = "SYSTEM ALERT: Resource usage exceeding threshold!\n"
        for key, value in metrics.items():
            if value >= threshold:
                alert_message += f"- {key.replace('_', ' ').title()}: {value}%\n"
        
        # Send alert
        if alert_config:
            method = alert_config.get('method', 'slack')
            alerts_sent = send_alert(alert_message, method, alert_config)
        
        # Close predefined processes if needed
        if predefined_processes:
            processes_closed = close_predefined_processes(predefined_processes)
    
    return {
        'metrics': metrics,
        'alerts_sent': alerts_sent,
        'processes_closed': processes_closed
    }