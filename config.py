# config.py
class Config:
    # Flask app configuration
    SECRET_KEY = 'your-secret-key-here'
    
    # Resource monitoring configuration
    RESOURCE_THRESHOLD = 90  # Threshold percentage for alerts
    MONITOR_INTERVAL = 1    # Check interval in seconds
    
    # Processes to close when threshold is exceeded
    PREDEFINED_PROCESSES_TO_CLOSE = [
        # Add process names to automatically close when resources are high
        # Example: 'chrome.exe', 'firefox.exe'
    ]
    
    # Alert configuration
    ALERT_METHOD = 'slack'  # 'slack' or 'whatsapp'
    SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/your/webhook/url'
    
    # WhatsApp configuration (if using WhatsApp alerts)
    WHATSAPP_TO = ''  # Recipient phone number
    WHATSAPP_FROM = ''  # Your WhatsApp number
    WHATSAPP_TOKEN = ''  # Auth token for WhatsApp API