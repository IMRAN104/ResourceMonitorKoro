import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    RESOURCE_USAGE_ALERT_THRESHOLD = 90  # Percentage
    DATA_COLLECTION_INTERVAL = 60  # In seconds
    SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
    WHATSAPP_API_URL = os.environ.get('WHATSAPP_API_URL')
    PREDEFINED_PROCESSES_TO_CLOSE = ['process_name_1', 'process_name_2']  # Add actual process names here
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///site.db'  # Example for SQLite database
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Enable debug mode based on environment variable