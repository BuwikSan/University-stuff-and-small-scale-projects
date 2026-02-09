"""
Konfigurace aplikace - Redis, MongoDB, Flask settings
"""
import os
from dotenv import load_dotenv

# Load environment variables z .env souboru
load_dotenv()

class Config:
    """Základní konfigurace"""
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-in-production")
    
    # Redis Configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/krizove_udalosti")
    MONGO_DB_NAME = "krizove_udalosti"
    MONGO_EVENTS_COLLECTION = "events"
    
    # Cache settings
    CACHE_TTL = 300  # 5 minut

class DevelopmentConfig(Config):
    """Vývoj - debug mode"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Produkce"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testování"""
    DEBUG = True
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/krizove_udalosti_test"

# Vybrat config na základě environment proměnné
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}
