# config.py
class Config:
    # Flask configuration
    SECRET_KEY = 'your-secret-key-change-this-in-production'
    DEBUG = True
    
    # Resource monitoring configuration
    RESOURCE_THRESHOLD = 90  # Percentage threshold for alerts
    PREDEFINED_PROCESSES_TO_CLOSE = [
        # Add process names to automatically close when resources are high
        # Example: 'chrome.exe', 'firefox.exe'
        'chrome.exe', 'notepad.exe'
    ]
    
    # Alert configuration
    ALERT_METHOD = 'slack'  # 'slack' or 'whatsapp'
    SLACK_WEBHOOK_URL = ''  # Add your webhook URL here