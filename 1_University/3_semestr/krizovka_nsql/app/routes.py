"""
Routes - všechny endpointy
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, current_app
from datetime import datetime, timedelta
import logging

from .models import CrisisEvent, CRISIS_TYPES

logger = logging.getLogger(__name__)

# Blueprinty
main_bp = Blueprint("main", __name__)
events_bp = Blueprint("events", __name__, url_prefix="/events")


# ==================== MAIN ROUTES ====================

@main_bp.route("/")
def index():
    """Homepage"""
    try:
        # Zkus načíst stats
        if current_app.db:
            total_events = current_app.db.count_events()
            today_events = current_app.db.count_today_events()
            latest_events = current_app.db.get_all_events(limit=6)
        else:
            total_events = 0
            today_events = 0
            latest_events = []
        
        return render_template(
            "dashboard.html",
            total_events=total_events,
            today_events=today_events,
            latest_events=latest_events,
            crisis_types=CRISIS_TYPES
        )
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template("dashboard.html", error="Chyba při načítání dat", 
                             total_events=0, today_events=0, latest_events=[], crisis_types=CRISIS_TYPES)


@main_bp.route("/health")
def health():
    """Health check endpoint"""
    if current_app.db:
        health = current_app.db.health_check()
        status = "ok" if all(health.values()) else "partial"
    else:
        health = {"mongo": False, "redis": False}
        status = "down"
    
    return jsonify({
        "status": status,
        "database": health
    })


# ==================== EVENTS ROUTES ====================

@events_bp.route("/submit", methods=["GET", "POST"])
def submit_event():
    """Formulář pro přidání nové crisis event"""
    
    if request.method == "POST":
        try:
            # Získej data z formuláře
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            location = request.form.get("location", "").strip()
            severity = int(request.form.get("severity", 1))
            event_type = request.form.get("type", "ostatní")
            
            # Validace
            if not all([title, description, location]):
                return render_template(
                    "submit_event.html",
                    crisis_types=CRISIS_TYPES,
                    error="Vyplň všechna povinná pole"
                ), 400
            
            # Vytvoř event
            event = CrisisEvent(
                title=title,
                description=description,
                location=location,
                severity=severity,
                event_type=event_type
            )
            
            # Ulož do DB
            if current_app.db:
                event_id = current_app.db.create_event(event)
                logger.info(f"✓ Event vytvořen: {event_id}")
                return redirect(url_for("events.view_all"))
            else:
                return render_template(
                    "submit_event.html",
                    crisis_types=CRISIS_TYPES,
                    error="Databáze není dostupná"
                ), 500
        
        except Exception as e:
            logger.error(f"Error submitting event: {e}")
            return render_template(
                "submit_event.html",
                crisis_types=CRISIS_TYPES,
                error=f"Chyba: {str(e)}"
            ), 500
    
    # GET - vrať formulář
    return render_template("submit_event.html", crisis_types=CRISIS_TYPES)


@events_bp.route("/view")
def view_all():
    """Zobraz všechny events"""
    try:
        # Pagination
        page = request.args.get("page", 1, type=int)
        limit = 10  # 10 na stránku pro lepší demo
        skip = (page - 1) * limit
        
        if current_app.db:
            events = current_app.db.get_all_events(limit=limit + 1, skip=skip)
            total = current_app.db.count_events()
            has_next = len(events) > limit
            events = events[:limit]
        else:
            events = []
            total = 0
            has_next = False
        
        return render_template(
            "view_events.html",
            events=events,
            page=page,
            has_next=has_next,
            total=total
        )
    except Exception as e:
        logger.error(f"Error viewing events: {e}")
        return render_template("view_events.html", error=str(e), events=[], page=1, has_next=False, total=0), 500


@events_bp.route("/<event_id>")
def view_event(event_id):
    """Zobraz detail eventu"""
    try:
        page = request.args.get("page", 1, type=int)  # Pamatuj si stránku
        if current_app.db:
            event = current_app.db.get_event(event_id)
            if not event:
                return render_template("error.html", message="Event nenalezen"), 404
            return render_template("event_detail.html", event=event, page=page)
        else:
            return render_template("error.html", message="Databáze není dostupná"), 500
    except Exception as e:
        logger.error(f"Error viewing event: {e}")
        return render_template("error.html", message=str(e)), 500


@events_bp.route("/<event_id>/delete", methods=["POST"])
def delete_event(event_id):
    """Smaž event (TODO: přidat auth)"""
    try:
        if current_app.db:
            success = current_app.db.delete_event(event_id)
            if success:
                return redirect(url_for("events.view_all"))
            else:
                return render_template("error.html", message="Event se nepodařilo smazat"), 400
        else:
            return render_template("error.html", message="Databáze není dostupná"), 500
    except Exception as e:
        logger.error(f"Error deleting event: {e}")
        return render_template("error.html", message=str(e)), 500


@events_bp.route("/api/stats")
def api_stats():
    """API endpoint - get stats v JSON"""
    try:
        if current_app.db:
            stats = {
                "total_events": current_app.db.count_events(),
                "events_by_severity": {
                    "critical": len(current_app.db.get_events_by_severity(5, 5)),
                    "high": len(current_app.db.get_events_by_severity(4, 4)),
                    "medium": len(current_app.db.get_events_by_severity(3, 3)),
                    "low": len(current_app.db.get_events_by_severity(1, 2)),
                }
            }
            return jsonify(stats)
        else:
            return jsonify({"error": "Database unavailable"}), 500
    except Exception as e:
        logger.error(f"API stats error: {e}")
        return jsonify({"error": str(e)}), 500
