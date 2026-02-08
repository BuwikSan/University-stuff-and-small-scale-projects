"""
Flask aplikace - inicializace
"""
from flask import Flask
import logging
import os

from .config import config
from .db import DatabaseManager


def create_app(config_name: str = None):
    """
    Application factory pattern - vytvoří Flask app s databází
    """
    
    # Vybrat config
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")
    
    app_config = config.get(config_name, config["default"])
    
    # Vytvor Flask app
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(app_config)
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Startuji app s config: {config_name}")
    
    # Databáze
    try:
        db = DatabaseManager(
            mongo_uri=app.config["MONGO_URI"],
            redis_url=app.config["REDIS_URL"],
            db_name=app.config["MONGO_DB_NAME"]
        )
        app.db = db
        logger.info("✓ Databáze inicializována")
    except Exception as e:
        logger.error(f"✗ Chyba při inicializaci DB: {e}")
        # Pokračuj i bez DB pro development
        app.db = None
    
    # Register blueprints (routes)
    from .routes import main_bp, events_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(events_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Server error: {error}")
        return {"error": "Internal server error"}, 500
    
    # Cleanup
    @app.teardown_appcontext
    def close_db(error):
        if hasattr(app, "db") and app.db:
            # Neuzavírej připojení, ponech je otevřená (connection pooling)
            pass
    
    return app
