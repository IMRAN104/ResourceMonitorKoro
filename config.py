# config.py
class Config:
    # Flask configuration
    SECRET_KEY = 'your-secret-key-change-this-in-production'
    DEBUG = True
    
    # Resource monitoring configuration
    RESOURCE_THRESHOLD = 90  # Percentage threshold for alerts
    
    # List of processes to automatically close when resources exceed threshold
    # Replace these with actual processes you want to close
    # Examples: 'chrome.exe', 'firefox.exe', 'notepad.exe', etc.
    PREDEFINED_PROCESSES_TO_CLOSE = [
        'notepad.exe',  # Example for Windows
        'CalculatorApp.exe',  # Example for Windows
        'rider64.exe',
        # For Linux users, you might want to use:
        # 'gedit',
        # 'gnome-calculator',
        # For Mac users:
        # 'TextEdit',
        # 'Calculator'
    ]
    
    # Alert configuration
    ALERT_METHOD = 'slack'  # 'slack' or 'whatsapp'
    SLACK_WEBHOOK_URL = ''  # Add your webhook URL here