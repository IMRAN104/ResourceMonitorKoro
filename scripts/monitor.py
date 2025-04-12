import psutil
import time
import requests
import json
from datetime import datetime

# Configuration
ALERT_THRESHOLD = 90  # Percentage
CHECK_INTERVAL = 60  # Seconds
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/your/slack/webhook'  # Replace with your Slack webhook URL
PREDEFINED_PROCESSES = ['process_name_1', 'process_name_2']  # Replace with actual process names to terminate

def send_alert(message):
    payload = {
        "text": message
    }
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

def terminate_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in PREDEFINED_PROCESSES:
            proc.terminate()

def collect_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    return {
        'timestamp': datetime.now().isoformat(),
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'top_processes': get_top_processes()
    }

def get_top_processes():
    processes = [(proc.info['name'], proc.info['cpu_percent']) for proc in psutil.process_iter(['name', 'cpu_percent'])]
    processes.sort(key=lambda x: x[1], reverse=True)
    return processes[:5]

def main():
    while True:
        metrics = collect_metrics()
        print(metrics)  # Replace with logic to store metrics in the database

        if metrics['cpu_usage'] >= ALERT_THRESHOLD or metrics['memory_usage'] >= ALERT_THRESHOLD:
            send_alert(f"Alert! Resource usage is high: CPU {metrics['cpu_usage']}%, Memory {metrics['memory_usage']}%")
            terminate_processes()

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()