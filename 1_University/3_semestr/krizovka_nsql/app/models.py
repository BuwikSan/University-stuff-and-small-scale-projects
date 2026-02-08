"""
Datový model pro Krize/Événementy
"""
from datetime import datetime
from typing import Optional, Dict, Any
import json

class CrisisEvent:
    """
    Model pro krizi/krízovou událost
    Schéma: title, description, location (GPS nebo text), severity (1-5), type, timestamp
    """
    
    def __init__(
        self,
        title: str,
        description: str,
        location: str,
        severity: int,
        event_type: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        _id: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ):
        self.title = title
        self.description = description
        self.location = location
        self.severity = min(5, max(1, severity))  # 1-5
        self.event_type = event_type
        self.latitude = latitude
        self.longitude = longitude
        self._id = _id
        self.created_at = created_at or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Konvertuj na dict pro MongoDB"""
        doc = {
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "severity": self.severity,
            "type": self.event_type,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "created_at": self.created_at,
        }
        # Jen přidej _id pokud není None (MongoDB si sám generuje ObjectId)
        if self._id is not None:
            doc["_id"] = self._id
        return doc
    
    def to_json(self) -> str:
        """Konvertuj na JSON string"""
        data = self.to_dict()
        data["created_at"] = data["created_at"].isoformat()
        return json.dumps(data, default=str)
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "CrisisEvent":
        """Vytvoř CrisisEvent z dict (z MongoDB)"""
        if isinstance(data.get("created_at"), str):
            created_at = datetime.fromisoformat(data["created_at"])
        else:
            created_at = data.get("created_at")
        
        return CrisisEvent(
            title=data.get("title"),
            description=data.get("description"),
            location=data.get("location"),
            severity=data.get("severity", 1),
            event_type=data.get("type", "other"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            _id=data.get("_id"),
            created_at=created_at,
        )


# Typy crisis eventů
CRISIS_TYPES = [
    "přírodní_katastrofa",  # Zemětřesení, záplava, etc
    "dopravní_nehoda",       # Auto, vlak, letadlo
    "požár",                  # Fire
    "zdravotnické_nouzové",  # Lékařský nouzový
    "průmyslová_havárie",    # Industrial accident
    "teroristický_útok",     # Terrorist attack
    "únos",                   # Kidnapping
    "ostatní"                 # Other
]
