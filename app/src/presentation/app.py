from flask import Flask
from ..config.container import Container
from .controllers.greeting_controller import greeting_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure container
    container = Container()
    container.wire(modules=["src.presentation.controllers.greeting_controller"])
    
    # Store container in app context for cleanup
    app.container = container
    
    # Register blueprints
    app.register_blueprint(greeting_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'hello-world-api'}, 200
    
    return app