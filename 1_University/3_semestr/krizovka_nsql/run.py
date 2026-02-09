#!/usr/bin/env python
"""
Spuštění Flask aplikace

Použití:
    python run.py                    # Development mode
    FLASK_ENV=production python run.py  # Production mode
"""

import os
import sys
from app import create_app

if __name__ == "__main__":
    # Vybrat environment
    env = os.environ.get("FLASK_ENV", "development")
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║       KrizeMapa - Crisis Manager       ║
    ║        Flask + MongoDB + Redis         ║
    ║                                        ║
    ║  Environment: {env.upper():<27}        ║
    ╚════════════════════════════════════════╝
    """)
    
    # Vytvoř app
    app = create_app(env)
    
    # Spusť development server
    debug = env == "development"
    host = os.environ.get("FLASK_HOST", "localhost")
    port = int(os.environ.get("FLASK_PORT", "5000"))
    
    print(f"\n Server running na http://{host}:{port}")
    print(f" Debug mode: {'ON' if debug else 'OFF'}\n")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        sys.exit(0)
