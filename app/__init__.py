# app/__init__.py
from flask import Flask
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config.from_object('config.Config')
    
    # Register blueprints
    from . import routes
    app.register_blueprint(routes.bp)
    
    # Log app startup
    logging.info('Flask app created and configured')
    
    return app